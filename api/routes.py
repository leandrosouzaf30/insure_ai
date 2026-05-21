"""
Rotas da API FastAPI para o chatbot RAG.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import shutil
from pathlib import Path
import uuid

from config import DOCS_DIR, FAQ_FILE, GEMINI_MODEL
from rag.loader import (
    load_documents,
)
from rag.retriever import (
    retrieve_relevant_chunks,
    build_context_from_chunks,
)
from rag.generator import (
    generate_response,
)
from rag.faq import (
    categorize_question,
    find_best_faq_answer,
    format_faq_context,
    load_faqs,
    summarize_faq_categories,
)
from rag.flows import (
    get_flow_by_category,
    get_initial_stage,
    get_next_stage,
    should_escalate,
    get_escalation_prompt,
    format_flow_context,
    track_flow_progress,
    FLOWS_MAP,
)
router = APIRouter()

# Armazena sessões de atendimento em memória (em produção, usar banco de dados)
_sessions: Dict[str, Dict] = {}


# ── Schemas ──────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000, description="Pergunta do usuário")
    top_k: int = Field(default=3, ge=1, le=10, description="Nº de chunks a recuperar")
    model: Optional[str] = Field(default=None, description="Modelo Gemini (sobrescreve o .env)")
    session_id: Optional[str] = Field(default=None, description="ID de sessão para rastrear fluxo")
    current_stage: Optional[str] = Field(default="inicial", description="Estágio atual do fluxo")


class ChatResponse(BaseModel):
    question: str
    answer: str
    model_used: str
    sources: List[str]
    intent: Optional[str] = None
    faq_match: bool = False
    retries: int
    error: Optional[str]
    session_id: str
    flow_category: Optional[str] = None
    current_stage: Optional[str] = None
    next_stage: Optional[str] = None
    flow_complete: bool = False
    requires_escalation: bool = False


class FAQItemResponse(BaseModel):
    question: str
    category: str
    tags: List[str]
    source: str


class DocumentInfo(BaseModel):
    filename: str
    path: str
    size: int


class StatusResponse(BaseModel):
    status: str
    model: str
    documents_loaded: int
    docs_dir: str


class FlowDetailResponse(BaseModel):
    category: str
    name: str
    priority: int
    stages_count: int
    requires_escalation_keywords: List[str]
    description: str


class FlowListResponse(BaseModel):
    flows: List[Dict]
    total_flows: int


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=StatusResponse, summary="Status da API")
async def health_check():
    """Verifica o status da API e quantos documentos estão carregados."""
    docs = load_documents(DOCS_DIR)
    return {
        "status": "online",
        "model": GEMINI_MODEL,
        "documents_loaded": len(docs),
        "docs_dir": DOCS_DIR,
    }


@router.post("/chat", response_model=ChatResponse, summary="Enviar pergunta ao chatbot RAG com fluxo")
async def chat(request: ChatRequest):
    """
    Endpoint principal do chatbot com suporte a fluxos de atendimento.
    1. Cria/recupera sessão e fluxo apropriado.
    2. Carrega documentos da base de conhecimento.
    3. Tenta corresponder a pergunta a uma FAQ categorizada.
    4. Recupera chunks relevantes e gera resposta com Gemini.
    5. Rastreia progresso no fluxo de atendimento.
    """
    # 1. Criar/recuperar sessão
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in _sessions:
        _sessions[session_id] = {
            "category": None,
            "stage": "inicial",
            "info_collected": {},
        }
    
    session = _sessions[session_id]
    
    # 2. Carregar contexto e FAQs
    documents = load_documents(DOCS_DIR)
    faqs = load_faqs(DOCS_DIR, filename=FAQ_FILE)
    faq_match = find_best_faq_answer(request.question, faqs)
    intent = faq_match["category"] if faq_match else categorize_question(request.question)
    
    # 3. Determinar/recuperar categoria e fluxo
    if not session["category"]:
        session["category"] = intent
    
    flow = get_flow_by_category(session["category"])
    
    # 4. Verificar se requer escalação
    requires_escalation = should_escalate(request.question, flow)
    escalation_response = ""
    if requires_escalation:
        escalation_response = get_escalation_prompt(session["category"], "Consulta prioritária detectada")
    
    # 5. Buscar contexto adicional nos documentos
    chunks = retrieve_relevant_chunks(
        query=request.question,
        documents=documents,
        top_k=request.top_k,
    )
    context = build_context_from_chunks(chunks)
    sources = [c["filename"] for c in chunks]
    
    # 6. Montar resposta priorizando FAQ quando houver correspondência direta
    flow_context = format_flow_context(flow)
    
    if faq_match:
        sources.append(faq_match.get("source", "FAQ de Seguros"))
        if faq_match["score"] >= 0.65:
            answer = (
                f"{faq_match['answer']}\n\n"
                f"Categoria: {faq_match['category']}"
            )
            if escalation_response:
                answer += f"\n\n{escalation_response}"
            
            progress = track_flow_progress(request.question, request.current_stage or session["stage"], flow)
            session["stage"] = progress["next_stage"] or session["stage"]
            
            return ChatResponse(
                question=request.question,
                answer=answer,
                model_used="FAQ_KB",
                sources=sources,
                intent=intent,
                faq_match=True,
                session_id=session_id,
                flow_category=flow.category,
                current_stage=progress["current_stage"],
                next_stage=progress["next_stage"],
                flow_complete=progress["flow_complete"],
                requires_escalation=requires_escalation,
                retries=0,
                error=None,
            )
        
        faq_context = format_faq_context(faq_match)
        full_context = f"{flow_context}\n\n{faq_context}\n\n{context}" if context else f"{flow_context}\n\n{faq_context}"
    else:
        full_context = f"{flow_context}\n\n{context}" if context else flow_context
    
    # 7. Gerar resposta com Gemini
    result = generate_response(
        question=request.question,
        context=full_context,
        model=request.model,
    )
    
    # 8. Rastrear progresso no fluxo
    progress = track_flow_progress(request.question, request.current_stage or session["stage"], flow)
    session["stage"] = progress["next_stage"] or session["stage"]
    
    final_answer = result["answer"]
    if escalation_response:
        final_answer += f"\n\n{escalation_response}"
    
    return ChatResponse(
        question=request.question,
        answer=final_answer,
        model_used=result["model_used"],
        sources=sources,
        intent=intent,
        faq_match=bool(faq_match),
        session_id=session_id,
        flow_category=flow.category,
        current_stage=progress["current_stage"],
        next_stage=progress["next_stage"],
        flow_complete=progress["flow_complete"],
        requires_escalation=requires_escalation,
        retries=result["retries"],
        error=result["error"],
    )


@router.get("/faq", response_model=List[FAQItemResponse], summary="Listar perguntas frequentes")
async def list_faqs():
    """Retorna a lista de FAQs carregadas da base de conhecimento."""
    return load_faqs(DOCS_DIR, filename=FAQ_FILE)


@router.get("/faq/categories", response_model=List[str], summary="Listar categorias de FAQ")
async def list_faq_categories():
    """Retorna as categorias de FAQ detectadas na base de conhecimento."""
    faqs = load_faqs(DOCS_DIR, filename=FAQ_FILE)
    return summarize_faq_categories(faqs)


@router.get("/documents", response_model=List[DocumentInfo], summary="Listar documentos carregados")
async def list_documents():
    """Lista todos os documentos disponíveis na base de conhecimento."""
    docs = load_documents(DOCS_DIR)
    return [
        DocumentInfo(filename=d["filename"], path=d["path"], size=d["size"])
        for d in docs
    ]


@router.post("/documents/upload", summary="Fazer upload de documento (.txt, .md, .csv, .json)")
async def upload_document(file: UploadFile = File(...)):
    """
    Faz upload de um novo documento para a base de conhecimento.
    Formatos aceitos: .txt, .md, .csv, .json
    """
    allowed = {".txt", ".md", ".csv", ".json"}
    ext = Path(file.filename).suffix.lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado: '{ext}'. Use: {', '.join(allowed)}",
        )

    dest = Path(DOCS_DIR) / file.filename
    dest.parent.mkdir(parents=True, exist_ok=True)

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"✅ Documento '{file.filename}' carregado com sucesso!", "path": str(dest)}


@router.delete("/documents/{filename}", summary="Remover documento da base")
async def delete_document(filename: str):
    """Remove um documento da base de conhecimento pelo nome do arquivo."""
    target = Path(DOCS_DIR) / filename
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"Arquivo '{filename}' não encontrado.")

    target.unlink()
    return {"message": f"🗑️ Documento '{filename}' removido com sucesso!"}


# ── Endpoints de Fluxos de Atendimento ───────────────────────────────────────

@router.get("/flows", response_model=FlowListResponse, summary="Listar fluxos de atendimento")
async def list_flows():
    """Retorna a lista de fluxos de atendimento disponíveis."""
    flows = []
    for category, flow in FLOWS_MAP.items():
        flows.append({
            "category": flow.category,
            "name": flow.name,
            "priority": flow.priority,
            "stages": len(flow.stages),
            "description": flow.context_prompt[:100] + "..." if flow.context_prompt else "Fluxo de atendimento padrão",
        })
    return FlowListResponse(flows=flows, total_flows=len(flows))


@router.get("/flows/{category}", response_model=FlowDetailResponse, summary="Detalhar fluxo específico")
async def get_flow_details(category: str):
    """Retorna os detalhes completos de um fluxo de atendimento."""
    flow = get_flow_by_category(category)
    
    return FlowDetailResponse(
        category=flow.category,
        name=flow.name,
        priority=flow.priority,
        stages_count=len(flow.stages),
        requires_escalation_keywords=flow.requires_escalation_keywords,
        description=flow.context_prompt,
    )


@router.get("/flows/{category}/stages", summary="Listar estágios de um fluxo")
async def get_flow_stages(category: str):
    """Retorna os estágios sequenciais de um fluxo de atendimento."""
    flow = get_flow_by_category(category)
    
    stages = []
    for i, stage in enumerate(flow.stages, 1):
        stages.append({
            "step": i,
            "stage": stage["stage"],
            "question": stage["question"],
            "required_info": stage.get("required_info", []),
        })
    
    return {
        "category": flow.category,
        "flow_name": flow.name,
        "total_stages": len(stages),
        "stages": stages,
    }


@router.post("/sessions/{session_id}/reset", summary="Resetar sessão de atendimento")
async def reset_session(session_id: str):
    """Reseta o estado de uma sessão de atendimento."""
    if session_id in _sessions:
        _sessions[session_id] = {
            "category": None,
            "stage": "inicial",
            "info_collected": {},
        }
        return {"message": f"✅ Sessão '{session_id}' resetada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail=f"Sessão '{session_id}' não encontrada.")


@router.get("/sessions/{session_id}", summary="Obter informações da sessão")
async def get_session_info(session_id: str):
    """Retorna o estado atual de uma sessão de atendimento."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail=f"Sessão '{session_id}' não encontrada.")
    
    session = _sessions[session_id]
    flow = get_flow_by_category(session["category"] or "atendimento")
    
    return {
        "session_id": session_id,
        "category": session["category"],
        "current_stage": session["stage"],
        "flow_name": flow.name,
        "info_collected": session["info_collected"],
    }