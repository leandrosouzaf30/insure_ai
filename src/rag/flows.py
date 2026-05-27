"""
Módulo de fluxos de atendimento conversacionais por tipo de consulta.
Define fluxos específicos para sinistro, apólice, cobertura, documentos, pagamento e atendimento.
"""

from typing import List, Optional, Dict
from enum import Enum


class FlowStage(Enum):
    """Estágios possíveis em um fluxo de atendimento."""
    INITIAL = "inicial"
    VALIDATION = "validacao"
    INFORMATION = "informacao"
    ACTION = "acao"
    CONFIRMATION = "confirmacao"
    ESCALATION = "escalacao"
    COMPLETED = "concluido"


class AttendanceFlow:
    """Define um fluxo de atendimento completo."""
    
    def __init__(
        self,
        category: str,
        name: str,
        priority: int,
        stages: List[Dict],
        validation_keywords: List[str],
        requires_escalation_keywords: List[str] = None,
        context_prompt: str = "",
    ):
        self.category = category
        self.name = name
        self.priority = priority  # 1 = urgente, 3 = baixa
        self.stages = stages
        self.validation_keywords = validation_keywords
        self.requires_escalation_keywords = requires_escalation_keywords or []
        self.context_prompt = context_prompt


# ── Fluxos de Atendimento Específicos ──────────────────────────────────────

FLOW_SINISTRO = AttendanceFlow(
    category="sinistro",
    name="Fluxo de Sinistro",
    priority=1,  # Urgente
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Entendi que você precisa registrar um sinistro. Quando o evento ocorreu?",
            "required_info": ["data", "local"],
        },
        {
            "stage": FlowStage.VALIDATION.value,
            "question": "Qual é o número da sua apólice? Precisamos validar sua cobertura.",
            "required_info": ["apolice_number"],
        },
        {
            "stage": FlowStage.INFORMATION.value,
            "question": "Descreva brevemente o que aconteceu (veículo, pessoa, propriedade?)",
            "required_info": ["tipo_dano", "descricao"],
        },
        {
            "stage": FlowStage.ACTION.value,
            "question": "Você possui boletim de ocorrência (BO) ou fotos do dano? Isso acelera o processo.",
            "required_info": ["documentos"],
        },
        {
            "stage": FlowStage.CONFIRMATION.value,
            "question": "Seu sinistro foi registrado. Um analista entrará em contato em até 24h. Referência: #SIN-{timestamp}",
            "required_info": [],
        },
    ],
    validation_keywords=["sinistro", "acidente", "ocorrência", "indenização", "dano"],
    requires_escalation_keywords=["urgente", "crítico", "morte", "incêndio", "assalto"],
    context_prompt="Você está sendo atendido em um fluxo prioritário de sinistro. Seja empático e colete todas as informações necessárias.",
)


FLOW_APOLICE = AttendanceFlow(
    category="apolice",
    name="Fluxo de Apólice",
    priority=2,
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Como posso ajudar com sua apólice? (renovação, cancelamento, dúvida?)",
            "required_info": ["tipo_solicitacao"],
        },
        {
            "stage": FlowStage.VALIDATION.value,
            "question": "Qual é o número da sua apólice?",
            "required_info": ["apolice_number"],
        },
        {
            "stage": FlowStage.INFORMATION.value,
            "question": "Me detalhe melhor sua solicitação.",
            "required_info": ["detalhes"],
        },
        {
            "stage": FlowStage.CONFIRMATION.value,
            "question": "Sua solicitação foi registrada. Você receberá confirmação por e-mail em até 2h úteis.",
            "required_info": [],
        },
    ],
    validation_keywords=["apólice", "contrato", "vencimento", "renovação", "cancelamento"],
    context_prompt="Fluxo de gerenciamento de apólice. Certifique-se de validar o número da apólice.",
)


FLOW_COBERTURA = AttendanceFlow(
    category="cobertura",
    name="Fluxo de Cobertura",
    priority=2,
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Qual tipo de cobertura você deseja consultar? (material, pessoal, assistência?)",
            "required_info": ["tipo_cobertura"],
        },
        {
            "stage": FlowStage.VALIDATION.value,
            "question": "Para esclarecer melhor, qual é o número da sua apólice?",
            "required_info": ["apolice_number"],
        },
        {
            "stage": FlowStage.INFORMATION.value,
            "question": "Descreva sua dúvida específica sobre a cobertura.",
            "required_info": ["duvida"],
        },
        {
            "stage": FlowStage.COMPLETED.value,
            "question": "Consulte sua apólice completa no portal do cliente ou fale com nosso atendimento para detalhes sobre exclusões.",
            "required_info": [],
        },
    ],
    validation_keywords=["cobertura", "assistência", "proteção", "risco", "incluso", "exclusão"],
    context_prompt="Fluxo de informações sobre cobertura. Forneça respostas claras sobre limites e exclusões.",
)


FLOW_DOCUMENTOS = AttendanceFlow(
    category="documentos",
    name="Fluxo de Documentos",
    priority=2,
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Qual documento você precisa? (comprovante, apólice, comprovante de pagamento?)",
            "required_info": ["tipo_documento"],
        },
        {
            "stage": FlowStage.VALIDATION.value,
            "question": "Qual é o seu e-mail ou telefone para enviarmos o documento?",
            "required_info": ["contato"],
        },
        {
            "stage": FlowStage.CONFIRMATION.value,
            "question": "Seu documento será enviado para {email} em até 24h.",
            "required_info": [],
        },
    ],
    validation_keywords=["documento", "comprovante", "carteira", "rg", "cpf", "apólice", "boleto"],
    context_prompt="Fluxo de solicitação de documentos. Seja rápido e eficiente.",
)


FLOW_PAGAMENTO = AttendanceFlow(
    category="pagamento",
    name="Fluxo de Pagamento",
    priority=3,
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Como posso ajudar com seu pagamento? (boleto vencido, parcelamento, segunda via?)",
            "required_info": ["tipo_pagamento"],
        },
        {
            "stage": FlowStage.VALIDATION.value,
            "question": "Qual é o número da sua apólice ou CPF?",
            "required_info": ["apolice_or_cpf"],
        },
        {
            "stage": FlowStage.INFORMATION.value,
            "question": "Qual é sua dúvida específica?",
            "required_info": ["detalhes"],
        },
        {
            "stage": FlowStage.CONFIRMATION.value,
            "question": "Entendido. Você pode gerar um novo boleto no portal ou falar com nosso atendimento.",
            "required_info": [],
        },
    ],
    validation_keywords=["pagamento", "boleto", "fatura", "parcelamento", "vencimento", "débito"],
    context_prompt="Fluxo de pagamento. Ofereça opções de parcelamento quando aplicável.",
)


FLOW_ATENDIMENTO = AttendanceFlow(
    category="atendimento",
    name="Fluxo de Atendimento Geral",
    priority=3,
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Olá! Como posso ajudá-lo hoje?",
            "required_info": ["assunto"],
        },
        {
            "stage": FlowStage.INFORMATION.value,
            "question": "Me detalhe melhor sua solicitação.",
            "required_info": ["detalhes"],
        },
        {
            "stage": FlowStage.CONFIRMATION.value,
            "question": "Obrigado pelo contato. Se precisar de mais informações, entre em contato conosco pelo telefone, e-mail ou chat.",
            "required_info": [],
        },
    ],
    validation_keywords=["contato", "telefone", "e-mail", "suporte", "ajuda", "atendimento", "dúvida"],
    context_prompt="Fluxo de atendimento geral. Seja prestativo e direcione para o fluxo correto quando necessário.",
)


# ── Mapeamento de Fluxos ──────────────────────────────────────────────────

FLOWS_MAP: Dict[str, AttendanceFlow] = {
    "sinistro": FLOW_SINISTRO,
    "apolice": FLOW_APOLICE,
    "cobertura": FLOW_COBERTURA,
    "documentos": FLOW_DOCUMENTOS,
    "pagamento": FLOW_PAGAMENTO,
    "atendimento": FLOW_ATENDIMENTO,
    "outros": FLOW_ATENDIMENTO,
}


# ── Funções de Gestão de Fluxos ───────────────────────────────────────────

def get_flow_by_category(category: str) -> AttendanceFlow:
    """Retorna o fluxo apropriado para uma categoria."""
    return FLOWS_MAP.get(category, FLOWS_MAP["atendimento"])


def get_next_stage(flow: AttendanceFlow, current_stage: str) -> Optional[Dict]:
    """Retorna o próximo estágio do fluxo."""
    stages = flow.stages
    for i, stage in enumerate(stages):
        if stage["stage"] == current_stage:
            if i + 1 < len(stages):
                return stages[i + 1]
            return None
    return stages[0] if stages else None


def get_initial_stage(flow: AttendanceFlow) -> Dict:
    """Retorna o estágio inicial de um fluxo."""
    return flow.stages[0] if flow.stages else {}


def should_escalate(question: str, flow: AttendanceFlow) -> bool:
    """Verifica se a pergunta requer escalação."""
    question_lower = question.lower()
    return any(
        keyword in question_lower 
        for keyword in flow.requires_escalation_keywords
    )


def get_escalation_prompt(category: str, reason: str = "") -> str:
    """Retorna mensagem de escalação appropriada."""
    flow = get_flow_by_category(category)
    escalation_msg = (
        f"Sua solicitação de {flow.name.lower()} foi identificada como prioritária"
        f" (Prioridade: {flow.priority}/3).\n"
    )
    if reason:
        escalation_msg += f"Motivo: {reason}\n"
    escalation_msg += (
        "Um especialista entrará em contato em breve. "
        "Referência: #ESC-{timestamp}"
    )
    return escalation_msg


def format_flow_context(flow: AttendanceFlow) -> str:
    """Monta contexto completo do fluxo para o LLM."""
    context = f"FLUXO DE ATENDIMENTO: {flow.name}\n"
    context += f"Prioridade: {flow.priority}/3\n"
    context += f"Etapas: {len(flow.stages)}\n\n"
    
    context += "Etapas do atendimento:\n"
    for i, stage in enumerate(flow.stages, 1):
        context += f"{i}. [{stage['stage'].upper()}] {stage['question']}\n"
    
    context += f"\n{flow.context_prompt}\n"
    return context


def track_flow_progress(
    question: str,
    current_stage: str,
    flow: AttendanceFlow,
) -> Dict:
    """Rastreia progresso no fluxo."""
    next_stage = get_next_stage(flow, current_stage)
    
    progress = {
        "current_stage": current_stage,
        "next_stage": next_stage["stage"] if next_stage else None,
        "next_question": next_stage["question"] if next_stage else None,
        "flow_complete": next_stage is None,
        "flow_category": flow.category,
        "requires_escalation": should_escalate(question, flow),
    }
    
    return progress
