"""
Rotas da API FastAPI para o chatbot RAG.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Optional
import shutil
from pathlib import Path

from config import DOCS_DIR, GEMINI_MODEL
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
router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000, description="Pergunta do usuário")
    top_k: int = Field(default=3, ge=1, le=10, description="Nº de chunks a recuperar")
    model: Optional[str] = Field(default=None, description="Modelo Gemini (sobrescreve o .env)")


class ChatResponse(BaseModel):
    question: str
    answer: str
    model_used: str
    sources: List[str]
    retries: int
    error: Optional[str]


class DocumentInfo(BaseModel):
    filename: str
    path: str
    size: int


class StatusResponse(BaseModel):
    status: str
    model: str
    documents_loaded: int
    docs_dir: str


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


@router.post("/chat", response_model=ChatResponse, summary="Enviar pergunta ao chatbot RAG")
async def chat(request: ChatRequest):
    """
    Endpoint principal do chatbot.
    1. Carrega documentos da base de conhecimento.
    2. Recupera chunks relevantes para a pergunta.
    3. Gera resposta com o Gemini usando o contexto recuperado.
    """
    # 1. Carregar documentos
    documents = load_documents(DOCS_DIR)

    # 2. Recuperar contexto relevante
    chunks = retrieve_relevant_chunks(
        query=request.question,
        documents=documents,
        top_k=request.top_k,
    )
    context = build_context_from_chunks(chunks)
    sources = [c["filename"] for c in chunks]

    # 3. Gerar resposta
    result = generate_response(
        question=request.question,
        context=context,
        model=request.model,
    )

    return ChatResponse(
        question=request.question,
        answer=result["answer"],
        model_used=result["model_used"],
        sources=sources,
        retries=result["retries"],
        error=result["error"],
    )


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