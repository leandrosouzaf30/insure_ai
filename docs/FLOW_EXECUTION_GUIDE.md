# 🚀 Guia Passo a Passo: Executar um Fluxo Completo

Guia completo para executar fluxos de atendimento na API do Chatbot RAG com Gemini.

---

## 📋 Pré-Requisitos

- ✅ Python 3.12+
- ✅ Poetry instalado
- ✅ Arquivo `.env` configurado com `GOOGLE_API_KEY`
- ✅ Terminal/CLI aberto

---

## ⚙️ Passo 1: Iniciar a Aplicação

### 1.1 Instalar Dependências (primeira vez)

```bash
cd /home/leandro/cursos/insurminds/desafio2/insure_ai
poetry install
```

### 1.2 Verificar Variáveis de Ambiente

```bash
# Verificar se .env existe
cat .env

# Deve conter:
# export GOOGLE_API_KEY="sua_chave_aqui"
# export GEMINI_MODEL="gemini-3-flash-preview"
```

### 1.3 Rodar a Aplicação

```bash
# Terminal 1: Rodar o servidor
poetry run uvicorn src.main:app --reload

# Saída esperada:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

### 1.4 Verificar Status da API

```bash
# Em outro terminal, testar conexão
curl http://localhost:8000/docs

# Deve abrir o Swagger UI da API
```

---

## 🎯 Passo 2: Entender os Fluxos Disponíveis

### 2.1 Listar Todos os Fluxos

```bash
curl -X GET http://localhost:8000/api/v1/flows
```

**Resposta:**

```json
{
  "flows": [
    {
      "category": "sinistro",
      "name": "Fluxo de Sinistro",
      "priority": 1,
      "stages_count": 5
    },
    {
      "category": "apolice",
      "name": "Fluxo de Apólice",
      "priority": 2,
      "stages_count": 4
    },
    {
      "category": "cobertura",
      "name": "Fluxo de Cobertura",
      "priority": 2,
      "stages_count": 4
    },
    {
      "category": "documentos",
      "name": "Fluxo de Documentos",
      "priority": 2,
      "stages_count": 3
    },
    {
      "category": "pagamento",
      "name": "Fluxo de Pagamento",
      "priority": 3,
      "stages_count": 4
    },
    {
      "category": "atendimento",
      "name": "Fluxo de Atendimento",
      "priority": 3,
      "stages_count": 3
    }
  ],
  "total_flows": 6
}
```

### 2.2 Obter Detalhes de um Fluxo Específico

```bash
# Detalhes do fluxo de sinistro
curl -X GET http://localhost:8000/api/v1/flows/sinistro
```

**Resposta:**

```json
{
  "category": "sinistro",
  "name": "Fluxo de Sinistro",
  "priority": 1,
  "stages_count": 5,
  "requires_escalation_keywords": [
    "urgente",
    "crítico",
    "morte",
    "incêndio",
    "assalto"
  ],
  "description": "Fluxo de atendimento para registrar sinistros com alta prioridade"
}
```

### 2.3 Obter Etapas de um Fluxo

```bash
# Etapas do fluxo de sinistro
curl -X GET http://localhost:8000/api/v1/flows/sinistro/stages
```

**Resposta:**

```json
{
  "category": "sinistro",
  "stages": [
    {
      "stage": "inicial",
      "question": "Entendi que você precisa registrar um sinistro. Quando o evento ocorreu?",
      "required_info": ["data", "local"]
    },
    {
      "stage": "validacao",
      "question": "Qual é o número da sua apólice? Precisamos validar sua cobertura.",
      "required_info": ["apolice_number"]
    },
    {
      "stage": "informacao",
      "question": "Descreva brevemente o que aconteceu (veículo, pessoa, propriedade?)",
      "required_info": ["tipo_dano", "descricao"]
    },
    {
      "stage": "acao",
      "question": "Você possui boletim de ocorrência (BO) ou fotos do dano? Isso acelera o processo.",
      "required_info": ["documentos"]
    },
    {
      "stage": "confirmacao",
      "question": "Seu sinistro foi registrado. Um analista entrará em contato em até 24h. Referência: #SIN-{timestamp}",
      "required_info": []
    }
  ]
}
```

---

## 💬 Passo 3: Executar um Fluxo Completo (Exemplo: Sinistro)

### 3.1 Primeiro Contato - Pergunta que Dispara Sinistro

```bash
# Request: Fazer uma pergunta que ativa o fluxo de sinistro
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu carro foi atingido por outro veículo ontem"
  }'
```

**Resposta:**

```json
{
  "question": "Meu carro foi atingido por outro veículo ontem",
  "answer": "Entendi que você precisa registrar um sinistro. Quando o evento ocorreu?",
  "model_used": "gemini-3-flash-preview",
  "sources": [],
  "intent": null,
  "faq_match": false,
  "retries": 0,
  "error": null,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "inicial",
  "next_stage": "validacao",
  "flow_complete": false,
  "requires_escalation": false
}
```

**⚠️ Importante:** Salve o `session_id` para continuar o fluxo!

```bash
export SESSION_ID="550e8400-e29b-41d4-a716-446655440000"
```

### 3.2 Segunda Mensagem - Validação (Estágio 2)

```bash
# Request: Responder a pergunta da etapa de validação
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Minha apólice é 123456789ABC\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"validacao\"
  }"
```

**Resposta:**

```json
{
  "question": "Minha apólice é 123456789ABC",
  "answer": "Obrigado. Sua apólice foi validada. Descreva brevemente o que aconteceu (veículo, pessoa, propriedade?)",
  "model_used": "gemini-3-flash-preview",
  "sources": [],
  "intent": null,
  "faq_match": false,
  "retries": 0,
  "error": null,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "validacao",
  "next_stage": "informacao",
  "flow_complete": false,
  "requires_escalation": false
}
```

### 3.3 Terceira Mensagem - Informação (Estágio 3)

```bash
# Request: Descrever o sinistro
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Um Fiat Uno azul 2015 colidiu no meu carro. Danos na lateral esquerda e capô amassado\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"informacao\"
  }"
```

**Resposta:**

```json
{
  "question": "Um Fiat Uno azul 2015 colidiu no meu carro. Danos na lateral esquerda e capô amassado",
  "answer": "Entendido. Você possui boletim de ocorrência (BO) ou fotos do dano? Isso acelera o processo.",
  "model_used": "gemini-3-flash-preview",
  "sources": [],
  "intent": null,
  "faq_match": false,
  "retries": 0,
  "error": null,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "informacao",
  "next_stage": "acao",
  "flow_complete": false,
  "requires_escalation": false
}
```

### 3.4 Quarta Mensagem - Ação (Estágio 4)

```bash
# Request: Fornecer documentos
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Tenho fotos do dano e o BO foi feito em delegacia. Número: BO/2026/054321\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"acao\"
  }"
```

**Resposta:**

```json
{
  "question": "Tenho fotos do dano e o BO foi feito em delegacia. Número: BO/2026/054321",
  "answer": "Perfeito! Seu sinistro foi registrado com sucesso. Um analista entrará em contato em até 24h. Referência: #SIN-20260527-001234",
  "model_used": "gemini-3-flash-preview",
  "sources": [],
  "intent": null,
  "faq_match": false,
  "retries": 0,
  "error": null,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "acao",
  "next_stage": "confirmacao",
  "flow_complete": true,
  "requires_escalation": false
}
```

✅ **Fluxo Concluído!** (`flow_complete: true`)

---

## 📊 Passo 4: Rastrear Status de uma Sessão

### 4.1 Obter Dados de uma Sessão

```bash
# Verificar estado completo da sessão
curl -X GET "http://localhost:8000/api/v1/sessions/$SESSION_ID"
```

**Resposta:**

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "confirmacao",
  "flow_complete": true,
  "requires_escalation": false,
  "messages_count": 4,
  "collected_info": {
    "data": "ontem",
    "local": "na rua",
    "apolice_number": "123456789ABC",
    "tipo_dano": "colisão lateral",
    "descricao": "Fiat Uno azul colidiu no meu carro",
    "documentos": "BO/2026/054321"
  },
  "created_at": "2026-05-27T10:30:00Z",
  "updated_at": "2026-05-27T10:35:00Z"
}
```

### 4.2 Resetar uma Sessão (Começar Novo Fluxo)

```bash
# Resetar sessão para iniciar novo fluxo
curl -X POST "http://localhost:8000/api/v1/sessions/$SESSION_ID/reset"
```

**Resposta:**

```json
{
  "status": "reset",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Sessão resetada. Pronto para novo fluxo."
}
```

---

## 🔥 Passo 5: Testar Escalação Automática

### 5.1 Pergunta que Ativa Escalação

```bash
# Pergunta com palavras-chave de urgência
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu seguro de vida é urgente! Faleceu um membro da família!"
  }'
```

**Resposta:**

```json
{
  "question": "Meu seguro de vida é urgente! Faleceu um membro da família!",
  "answer": "🚨 CASO CRÍTICO DETECTADO 🚨\n\nEntendo que você está passando por um momento difícil. Seu caso foi marcado como URGENTE e será atendido imediatamente por um especialista.",
  "model_used": "gemini-3-flash-preview",
  "sources": [],
  "intent": null,
  "faq_match": false,
  "retries": 0,
  "error": null,
  "session_id": "770e8400-e29b-41d4-a716-446655440001",
  "flow_category": "sinistro",
  "current_stage": "inicial",
  "next_stage": "validacao",
  "flow_complete": false,
  "requires_escalation": true,
  "priority_level": "critical"
}
```

⚠️ Note: `requires_escalation: true`

---

## 📝 Passo 6: Exemplo Completo com Script

### 6.1 Script Bash para Automatizar Fluxo

Crie arquivo `execute_flow.sh`:

```bash
#!/bin/bash

# Configuração
API_URL="http://localhost:8000/api/v1"
SESSION_ID=""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Teste de Fluxo Completo ===${NC}\n"

# Passo 1: Listar fluxos
echo -e "${YELLOW}1. Listando fluxos disponíveis...${NC}"
curl -s "$API_URL/flows" | jq '.flows[] | {category, name, priority}'
echo ""

# Passo 2: Primeira pergunta
echo -e "${YELLOW}2. Iniciando fluxo de sinistro...${NC}"
RESPONSE=$(curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu carro teve um acidente urgente! Foi atingido por um incêndio!"
  }')

SESSION_ID=$(echo $RESPONSE | jq -r '.session_id')
FLOW=$(echo $RESPONSE | jq -r '.flow_category')
ESCALATION=$(echo $RESPONSE | jq -r '.requires_escalation')

echo -e "${GREEN}✓ Session ID: $SESSION_ID${NC}"
echo -e "${GREEN}✓ Fluxo: $FLOW${NC}"
echo -e "${GREEN}✓ Escalação: $ESCALATION${NC}"
echo ""

# Passo 3: Segunda pergunta
echo -e "${YELLOW}3. Respondendo pergunta de validação...${NC}"
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Apólice 987654321XYZ\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"validacao\"
  }" | jq '.answer'
echo ""

# Passo 4: Checar estado da sessão
echo -e "${YELLOW}4. Estado atual da sessão...${NC}"
curl -s "$API_URL/sessions/$SESSION_ID" | jq '{
  session_id,
  flow_category,
  current_stage,
  flow_complete,
  requires_escalation
}'

echo -e "\n${GREEN}=== Teste Concluído ===${NC}"
```

### 6.2 Executar Script

```bash
chmod +x execute_flow.sh
./execute_flow.sh
```

---

## 🎓 Passo 7: Testar Todos os Fluxos

### 7.1 Fluxo de Apólice

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Preciso renovar minha apólice de seguro"
  }'
```

### 7.2 Fluxo de Cobertura

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu seguro cobre roubo? Quais são as exclusões?"
  }'
```

### 7.3 Fluxo de Pagamento

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Como faço para parcelar o pagamento do meu boleto?"
  }'
```

### 7.4 Fluxo de Documentos

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Que documentos preciso para abrir um sinistro?"
  }'
```

### 7.5 Fluxo de Atendimento Geral

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Como posso entrar em contato com o suporte?"
  }'
```

---

## 🛠️ Passo 8: Dicas e Boas Práticas

### 8.1 Use Postman para Testes Visuais

1. Abra Postman
2. Importe: `http://localhost:8000/docs`
3. Teste endpoints através da interface gráfica

### 8.2 Monitorar Logs da Aplicação

```bash
# Terminal rodando uvicorn mostra logs em tempo real
# Você verá:
# INFO:     127.0.0.1:54321 - "POST /api/v1/chat HTTP/1.1" 200 OK
```

### 8.3 Validar Respostas JSON

```bash
# Use jq para formatar e filtrar respostas
curl -s http://localhost:8000/api/v1/flows | jq '.flows[] | .category'
```

### 8.4 Salvar Responses em Arquivo

```bash
# Salvar response de um fluxo
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Preciso de um sinistro"}' \
  > response.json

# Visualizar arquivo
cat response.json | jq
```

---

## ❌ Tratamento de Erros

### Erro: 404 - Fluxo Não Encontrado

```bash
curl -X GET http://localhost:8000/api/v1/flows/fluxo_invalido
```

**Resposta:**

```json
{
  "detail": "Fluxo 'fluxo_invalido' não encontrado"
}
```

**Solução**: Use um dos fluxos válidos: `sinistro`, `apolice`, `cobertura`, `documentos`, `pagamento`, `atendimento`

### Erro: 422 - Validação de Dados

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question":""}'  # Vazio
```

**Resposta:**

```json
{
  "detail": [{
    "field": "question",
    "message": "Question must be at least 1 character"
  }]
}
```

**Solução**: Envie uma pergunta com pelo menos 1 caractere

### Erro: 500 - Erro do Servidor

Se receber 500, verifique:
1. ✅ API está rodando?
2. ✅ `.env` configurado?
3. ✅ Chave de API válida?
4. ✅ Verifique logs da aplicação

---

## 📊 Estrutura de Resposta Completa

Toda resposta do `/api/v1/chat` contém:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `question` | string | Pergunta do usuário |
| `answer` | string | Resposta do modelo |
| `model_used` | string | Modelo Gemini utilizado |
| `sources` | array | Documentos consultados |
| `session_id` | string | ID único da sessão (usar para continuar) |
| `flow_category` | string | Tipo de fluxo detectado |
| `current_stage` | string | Etapa atual do fluxo |
| `next_stage` | string | Próxima etapa esperada |
| `flow_complete` | boolean | Fluxo foi concluído? |
| `requires_escalation` | boolean | Requer escalação? |

---

## 🎯 Checklist de Execução

- [ ] Aplicação rodando na porta 8000
- [ ] `.env` configurado com chave de API
- [ ] Conseguiu listar fluxos (`GET /flows`)
- [ ] Iniciou um fluxo (recebeu `session_id`)
- [ ] Continuou fluxo com `session_id`
- [ ] Completou um fluxo inteiro
- [ ] Verificou estado da sessão (`GET /sessions/{session_id}`)
- [ ] Testou escalação automática
- [ ] Resetou uma sessão

---

## 📞 Referência Rápida de Endpoints

```bash
# Listar fluxos
GET /api/v1/flows

# Detalhes de um fluxo
GET /api/v1/flows/{category}

# Etapas do fluxo
GET /api/v1/flows/{category}/stages

# Chat (iniciar ou continuar)
POST /api/v1/chat

# Estado da sessão
GET /api/v1/sessions/{session_id}

# Resetar sessão
POST /api/v1/sessions/{session_id}/reset
```

---

**Próximo?** Explore `docs/EXAMPLES_API_CALLS.md` para mais exemplos avançados.
