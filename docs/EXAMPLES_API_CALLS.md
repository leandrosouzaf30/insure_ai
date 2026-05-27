"""
Exemplos de Uso: Fluxos de Atendimento na API

Execute os comandos curl abaixo para testar os fluxos em ação.
Certifique-se de que a API está rodando: uvicorn main:app --reload
"""

# ═══════════════════════════════════════════════════════════════════════════
# 1. LISTAR FLUXOS DISPONÍVEIS
# ═══════════════════════════════════════════════════════════════════════════

curl http://localhost:8000/api/v1/flows | jq .

# Esperado:
# {
#   "flows": [
#     {
#       "category": "sinistro",
#       "name": "Fluxo de Sinistro",
#       "priority": 1,
#       "stages": 5,
#       "description": "Você está sendo atendido em um fluxo prioritário de sinistro..."
#     },
#     ... (5 outros fluxos)
#   ],
#   "total_flows": 6
# }


# ═══════════════════════════════════════════════════════════════════════════
# 2. VER DETALHES DE UM FLUXO ESPECÍFICO
# ═══════════════════════════════════════════════════════════════════════════

curl http://localhost:8000/api/v1/flows/sinistro | jq .

# Esperado:
# {
#   "category": "sinistro",
#   "name": "Fluxo de Sinistro",
#   "priority": 1,
#   "stages_count": 5,
#   "requires_escalation_keywords": ["urgente", "crítico", "morte", "incêndio", "assalto"],
#   "description": "Você está sendo atendido em um fluxo prioritário de sinistro..."
# }


# ═══════════════════════════════════════════════════════════════════════════
# 3. LISTAR ETAPAS DE UM FLUXO
# ═══════════════════════════════════════════════════════════════════════════

curl http://localhost:8000/api/v1/flows/sinistro/stages | jq .

# Esperado:
# {
#   "category": "sinistro",
#   "flow_name": "Fluxo de Sinistro",
#   "total_stages": 5,
#   "stages": [
#     {
#       "step": 1,
#       "stage": "inicial",
#       "question": "Entendi que você precisa registrar um sinistro. Quando o evento ocorreu?",
#       "required_info": ["data", "local"]
#     },
#     ...
#   ]
# }


# ═══════════════════════════════════════════════════════════════════════════
# 4. INICIAR FLUXO DE SINISTRO (NOVA SESSÃO)
# ═══════════════════════════════════════════════════════════════════════════

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu carro foi atingido! Preciso registrar um sinistro urgente!",
    "top_k": 3
  }' | jq .

# Esperado:
# {
#   "session_id": "550e8400-e29b-41d4-a716-446655440001",
#   "flow_category": "sinistro",
#   "current_stage": "inicial",
#   "next_stage": "validacao",
#   "flow_complete": false,
#   "requires_escalation": true,
#   "question": "Meu carro foi atingido! Preciso registrar um sinistro urgente!",
#   "answer": "Entendo que você teve um acidente urgente. Lamento pelo ocorrido...",
#   "model_used": "gemini-3-flash-preview",
#   "sources": ["faqs.json"],
#   "intent": "sinistro",
#   "faq_match": true,
#   "retries": 0,
#   "error": null
# }


# ═══════════════════════════════════════════════════════════════════════════
# 5. CONTINUAR FLUXO DE SINISTRO (MESMA SESSÃO)
# ═══════════════════════════════════════════════════════════════════════════

# IMPORTANTE: Copie o session_id da resposta anterior

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Ontem às 14h na Vila Mariana, São Paulo",
    "session_id": "550e8400-e29b-41d4-a716-446655440001",
    "current_stage": "validacao",
    "top_k": 3
  }' | jq .

# Esperado:
# {
#   "session_id": "550e8400-e29b-41d4-a716-446655440001",
#   "flow_category": "sinistro",
#   "current_stage": "validacao",
#   "next_stage": "informacao",
#   "flow_complete": false,
#   "requires_escalation": true,
#   "question": "Ontem às 14h na Vila Mariana, São Paulo",
#   "answer": "Obrigado pelas informações. Agora preciso do número da sua apólice...",
#   "model_used": "gemini-3-flash-preview",
#   ...
# }


# ═══════════════════════════════════════════════════════════════════════════
# 6. CONSULTAR ESTADO DA SESSÃO
# ═══════════════════════════════════════════════════════════════════════════

curl http://localhost:8000/api/v1/sessions/550e8400-e29b-41d4-a716-446655440001 | jq .

# Esperado:
# {
#   "session_id": "550e8400-e29b-41d4-a716-446655440001",
#   "category": "sinistro",
#   "current_stage": "validacao",
#   "flow_name": "Fluxo de Sinistro",
#   "info_collected": {
#     "data": "20/05/2026",
#     "local": "Vila Mariana, São Paulo"
#   }
# }


# ═══════════════════════════════════════════════════════════════════════════
# 7. RESETAR SESSÃO
# ═══════════════════════════════════════════════════════════════════════════

curl -X POST http://localhost:8000/api/v1/sessions/550e8400-e29b-41d4-a716-446655440001/reset | jq .

# Esperado:
# {
#   "message": "✅ Sessão '550e8400-e29b-41d4-a716-446655440001' resetada com sucesso!"
# }


# ═══════════════════════════════════════════════════════════════════════════
# 8. TESTAR FLUXO DE APÓLICE
# ═══════════════════════════════════════════════════════════════════════════

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Como faço para renovar minha apólice?",
    "top_k": 3
  }' | jq .

# Esperado:
# {
#   "session_id": "novo-uuid",
#   "flow_category": "apolice",
#   "current_stage": "inicial",
#   "next_stage": "validacao",
#   "requires_escalation": false,
#   "answer": "Como posso ajudar com sua apólice?...",
#   ...
# }


# ═══════════════════════════════════════════════════════════════════════════
# 9. TESTAR FLUXO DE COBERTURA
# ═══════════════════════════════════════════════════════════════════════════

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "O que está coberto pela minha apólice?",
    "top_k": 3
  }' | jq .

# Esperado:
# {
#   "flow_category": "cobertura",
#   ...
# }


# ═══════════════════════════════════════════════════════════════════════════
# 10. TESTAR FLUXO DE DOCUMENTOS
# ═══════════════════════════════════════════════════════════════════════════

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Preciso de uma 2ª via do meu boleto",
    "top_k": 3
  }' | jq .

# Esperado:
# {
#   "flow_category": "documentos",
#   ...
# }


# ═══════════════════════════════════════════════════════════════════════════
# 11. TESTAR FLUXO DE PAGAMENTO
# ═══════════════════════════════════════════════════════════════════════════

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu boleto venceu, posso parcelar?",
    "top_k": 3
  }' | jq .

# Esperado:
# {
#   "flow_category": "pagamento",
#   ...
# }


# ═══════════════════════════════════════════════════════════════════════════
# 12. TESTE COMPLETO: FLUXO DE SINISTRO (5 MENSAGENS)
# ═══════════════════════════════════════════════════════════════════════════

# Passo 1: Iniciar
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Tive um acidente de trânsito!"
  }' | jq -r '.session_id')

echo "Session ID: $SESSION_ID"

# Passo 2: Fornecer data e local
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Ontem às 15h em Pinheiros\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"validacao\"
  }" | jq '.answer'

# Passo 3: Fornecer apólice
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Minha apólice é POL-123456\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"informacao\"
  }" | jq '.answer'

# Passo 4: Descrever dano
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Bati a lateral do carro em outro veículo\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"acao\"
  }" | jq '.answer'

# Passo 5: Fornecer documentos
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Tenho fotos e o boletim de ocorrência\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"confirmacao\"
  }" | jq '.answer'

# Consultar estado final
echo "Estado final da sessão:"
curl -s http://localhost:8000/api/v1/sessions/$SESSION_ID | jq .


# ═══════════════════════════════════════════════════════════════════════════
# 13. TESTE SHELL SCRIPT (Salvar como test_flows.sh)
# ═══════════════════════════════════════════════════════════════════════════

#!/bin/bash

API_URL="http://localhost:8000/api/v1"

echo "🧪 Testando Fluxos de Atendimento..."
echo ""

# 1. Listar fluxos
echo "1️⃣  Listando fluxos disponíveis..."
curl -s $API_URL/flows | jq '.flows[].name'
echo ""

# 2. Novo sinistro
echo "2️⃣  Iniciando novo sinistro..."
RESPONSE=$(curl -s -X POST $API_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Preciso registrar um sinistro"}')

SESSION_ID=$(echo $RESPONSE | jq -r '.session_id')
FLOW=$(echo $RESPONSE | jq -r '.flow_category')
STAGE=$(echo $RESPONSE | jq -r '.current_stage')

echo "   Session: $SESSION_ID"
echo "   Flow: $FLOW"
echo "   Stage: $STAGE"
echo ""

# 3. Consultar sessão
echo "3️⃣  Consultando estado da sessão..."
curl -s $API_URL/sessions/$SESSION_ID | jq '.current_stage'
echo ""

echo "✅ Testes concluídos!"


# ═══════════════════════════════════════════════════════════════════════════
# 14. PYTHON: Cliente para testar fluxos
# ═══════════════════════════════════════════════════════════════════════════

import requests
import json
import time

class FlowTester:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session_id = None
    
    def list_flows(self):
        response = requests.get(f"{self.base_url}/flows")
        return response.json()
    
    def send_message(self, question, current_stage="inicial"):
        data = {
            "question": question,
            "session_id": self.session_id,
            "current_stage": current_stage,
            "top_k": 3
        }
        response = requests.post(f"{self.base_url}/chat", json=data)
        result = response.json()
        
        # Armazenar session_id para próximas mensagens
        if not self.session_id:
            self.session_id = result.get("session_id")
        
        return result
    
    def get_session_info(self):
        if not self.session_id:
            return None
        response = requests.get(f"{self.base_url}/sessions/{self.session_id}")
        return response.json()
    
    def reset_session(self):
        if self.session_id:
            requests.post(f"{self.base_url}/sessions/{self.session_id}/reset")
            self.session_id = None

# Exemplo de uso:
# tester = FlowTester()
# result = tester.send_message("Tive um acidente")
# print(f"Flow: {result['flow_category']}")
# print(f"Stage: {result['current_stage']}")
# print(f"Answer: {result['answer']}")

""")
