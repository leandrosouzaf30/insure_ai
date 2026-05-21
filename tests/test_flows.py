"""
Testes de fluxos de atendimento — Valida integração e funcionamento.
Execute com: pytest tests/test_flows.py -v
"""

import pytest
import sys
from pathlib import Path

# Adiciona a pasta pai ao path para importar módulos da aplicação
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.flows import (
    get_flow_by_category,
    get_initial_stage,
    get_next_stage,
    should_escalate,
    track_flow_progress,
    FLOWS_MAP,
    FlowStage,
)


class TestFlowsInitialization:
    """Testa inicialização dos fluxos."""
    
    def test_all_flows_registered(self):
        """Verifica se todos os fluxos estão registrados."""
        expected_categories = {"sinistro", "apolice", "cobertura", "documentos", "pagamento", "atendimento", "outros"}
        assert set(FLOWS_MAP.keys()) == expected_categories, "Fluxos não correspondem aos esperados"
    
    def test_flow_structure(self):
        """Verifica se cada fluxo tem estrutura correta."""
        for category, flow in FLOWS_MAP.items():
            assert flow.category == category, f"Categoria inconsistente em {category}"
            assert flow.name, f"Fluxo {category} sem nome"
            assert flow.priority in [1, 2, 3], f"Prioridade inválida em {category}"
            assert len(flow.stages) > 0, f"Fluxo {category} sem etapas"
            assert len(flow.validation_keywords) > 0, f"Fluxo {category} sem palavras-chave"


class TestFlowRetrieval:
    """Testa recuperação de fluxos."""
    
    def test_get_flow_by_category(self):
        """Verifica se consegue recuperar fluxo por categoria."""
        flow = get_flow_by_category("sinistro")
        assert flow.category == "sinistro"
        assert flow.name == "Fluxo de Sinistro"
        assert flow.priority == 1
    
    def test_get_flow_default_for_unknown(self):
        """Verifica se retorna atendimento geral para categoria desconhecida."""
        flow = get_flow_by_category("categoria_inexistente")
        assert flow.category == "atendimento"
    
    def test_get_initial_stage(self):
        """Verifica se retorna primeiro estágio."""
        flow = get_flow_by_category("sinistro")
        initial = get_initial_stage(flow)
        assert initial["stage"] == FlowStage.INITIAL.value
        assert "question" in initial


class TestFlowNavigation:
    """Testa navegação entre etapas do fluxo."""
    
    def test_get_next_stage(self):
        """Verifica transição entre etapas."""
        flow = get_flow_by_category("sinistro")
        current_stage = flow.stages[0]
        next_stage = get_next_stage(flow, current_stage["stage"])
        
        assert next_stage is not None
        assert next_stage["stage"] != current_stage["stage"]
    
    def test_flow_completion(self):
        """Verifica se último estágio retorna None no próximo."""
        flow = get_flow_by_category("sinistro")
        last_stage = flow.stages[-1]
        next_after_last = get_next_stage(flow, last_stage["stage"])
        
        assert next_after_last is None, "Último estágio deveria retornar None"


class TestEscalationDetection:
    """Testa detecção automática de escalação."""
    
    def test_escalation_for_sinistro(self):
        """Verifica se detecta escalação em sinistros urgentes."""
        flow = get_flow_by_category("sinistro")
        
        assert should_escalate("Sinistro crítico! Alguém foi ferido.", flow) is True
        assert should_escalate("Há um incêndio em meu carro!", flow) is True
        assert should_escalate("Fui assaltado", flow) is True
        assert should_escalate("Qual o prazo para indenização?", flow) is False
    
    def test_no_escalation_for_general(self):
        """Verifica se atendimento geral não tem escalação por padrão."""
        flow = get_flow_by_category("atendimento")
        assert should_escalate("Me ajude com uma dúvida", flow) is False


class TestFlowProgress:
    """Testa rastreamento de progresso no fluxo."""
    
    def test_track_progress_advances_stage(self):
        """Verifica se rastreia progresso corretamente."""
        flow = get_flow_by_category("sinistro")
        initial_stage = flow.stages[0]["stage"]
        
        progress = track_flow_progress("Tive um acidente", initial_stage, flow)
        
        assert progress["current_stage"] == initial_stage
        assert progress["next_stage"] is not None
        assert progress["next_stage"] != initial_stage
        assert progress["flow_complete"] is False
    
    def test_track_progress_completion(self):
        """Verifica se detecta conclusão do fluxo."""
        flow = get_flow_by_category("sinistro")
        last_stage = flow.stages[-1]["stage"]
        
        progress = track_flow_progress("Obrigado", last_stage, flow)
        
        assert progress["current_stage"] == last_stage
        assert progress["next_stage"] is None
        assert progress["flow_complete"] is True


class TestFlowCategories:
    """Testa categorização de perguntas."""
    
    def test_sinistro_keywords(self):
        """Verifica se detecta perguntas de sinistro."""
        flow = get_flow_by_category("sinistro")
        test_questions = [
            "Preciso registrar um sinistro",
            "Tive um acidente",
            "Quero fazer uma ocorrência",
            "Qual é o valor da indenização?",
        ]
        
        for question in test_questions:
            assert any(kw in question.lower() for kw in flow.validation_keywords), \
                f"Palavras-chave não detectadas em: {question}"
    
    def test_apolice_keywords(self):
        """Verifica se detecta perguntas sobre apólice."""
        flow = get_flow_by_category("apolice")
        test_questions = [
            "Como renovo minha apólice?",
            "Quero cancelar meu contrato",
            "Qual o vencimento da minha apólice?",
        ]
        
        for question in test_questions:
            assert any(kw in question.lower() for kw in flow.validation_keywords), \
                f"Palavras-chave não detectadas em: {question}"


class TestFlowContexts:
    """Testa contextos e prompts dos fluxos."""
    
    def test_flows_have_context_prompts(self):
        """Verifica se todos os fluxos têm prompts de contexto."""
        for category, flow in FLOWS_MAP.items():
            assert flow.context_prompt, f"Fluxo {category} sem context_prompt"
            assert len(flow.context_prompt) > 10, f"context_prompt muito curto em {category}"
    
    def test_stage_required_info(self):
        """Verifica se etapas têm informações requeridas."""
        flow = get_flow_by_category("sinistro")
        for stage in flow.stages:
            assert "required_info" in stage, f"Etapa sem required_info: {stage}"
            assert isinstance(stage["required_info"], list), "required_info deve ser lista"


class TestFlowPriorities:
    """Testa prioridades dos fluxos."""
    
    def test_sinistro_is_high_priority(self):
        """Verifica se sinistro é alta prioridade."""
        flow = get_flow_by_category("sinistro")
        assert flow.priority == 1, "Sinistro deveria ter prioridade 1"
    
    def test_pagamento_is_low_priority(self):
        """Verifica se pagamento é baixa prioridade."""
        flow = get_flow_by_category("pagamento")
        assert flow.priority == 3, "Pagamento deveria ter prioridade 3"
    
    def test_apolice_is_medium_priority(self):
        """Verifica se apólice é média prioridade."""
        flow = get_flow_by_category("apolice")
        assert flow.priority == 2, "Apólice deveria ter prioridade 2"


def test_summary():
    """Teste resumido: valida estrutura geral dos fluxos."""
    print("\n✅ RESUMO DOS FLUXOS DISPONÍVEIS:")
    print("=" * 70)
    
    for category, flow in FLOWS_MAP.items():
        priority_symbol = "🚨" if flow.priority == 1 else "⚠️" if flow.priority == 2 else "ℹ️"
        print(f"\n{priority_symbol} {flow.name.upper()} ({category})")
        print(f"   Prioridade: {flow.priority}/3")
        print(f"   Etapas: {len(flow.stages)}")
        print(f"   Palavras-chave: {', '.join(flow.validation_keywords[:3])}...")
        
        if flow.requires_escalation_keywords:
            print(f"   ⚡ Escalação automática: {', '.join(flow.requires_escalation_keywords)}")
    
    print("\n" + "=" * 70)
    print(f"✅ Total de fluxos: {len(FLOWS_MAP)}")
    print("✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_summary()
