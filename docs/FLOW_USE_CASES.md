# 🧪 Casos de Uso Práticos e Testes

Exemplos reais de casos de uso e como testá-los na API.

---

## 🚨 Caso de Uso 1: Sinistro Urgente (Incêndio)

### Cenário
Cliente com seguro de veículo tem seu carro atingido por incêndio e precisa registrar sinistro com urgência.

### Passo a Passo

#### 1. Fazer Pergunta com Urgência

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "URGENTE! Meu carro está pegando fogo no acostamento da BR-116!"
  }'
```

**Resposta Esperada:**
```json
{
  "question": "URGENTE! Meu carro está pegando fogo no acostamento da BR-116!",
  "answer": "🚨 EMERGÊNCIA DETECTADA 🚨\n\nSeu caso foi marcado como CRÍTICO. Um especialista acompanhará você pessoalmente.",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "inicial",
  "requires_escalation": true,
  "priority_level": "critical"
}
```

✅ **Validação**: `requires_escalation: true`

#### 2. Confirmar Apólice

```bash
SESSION_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Minha apólice é APO-2024-987654321\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"validacao\"
  }"
```

#### 3. Descrever Sinistro

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Hyundai HB20 branco, placa ABC-1234, total perda pela queimadura. Tive que sair correndo!\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"informacao\"
  }"
```

#### 4. Confirmar Documentos

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Tenho vídeo do fogo, BO feito na delegacia (número 2026/009876) e vou tirar fotos agora\",
    \"session_id\": \"$SESSION_ID\",
    \"current_stage\": \"acao\"
  }"
```

**Resposta Final:**
```json
{
  "answer": "Sinistro crítico registrado com sucesso! Referência: #SIN-20260527-CRITICAL-001\nTim especialista em sinistros de incêndio ligará em MÁXIMO 30 minutos no número registrado.",
  "flow_complete": true,
  "requires_escalation": true
}
```

---

## 📋 Caso de Uso 2: Renovação de Apólice

### Cenário
Cliente deseja renovar sua apólice de seguro residencial que vence em 30 dias.

### Teste

```bash
# 1. Pergunta inicial
RESP=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Preciso renovar minha apólice de seguro residencial"}')

SESSION=$(echo $RESP | jq -r '.session_id')
echo "Session: $SESSION"
echo "Response: $(echo $RESP | jq -r '.answer')"

# 2. Informar número da apólice
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Número: SEG-RES-2024-001122\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"validacao\"
  }" | jq '.answer'

# 3. Confirmar renovação
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Quero renovar com as mesmas coberturas de sempre\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"informacao\"
  }" | jq '.answer'

# 4. Verificar conclusão
curl -s -X GET "http://localhost:8000/api/v1/sessions/$SESSION" | jq '{
  flow_complete,
  flow_category,
  collected_info
}'
```

**Resposta Esperada:**
```json
{
  "flow_complete": true,
  "flow_category": "apolice",
  "collected_info": {
    "tipo_solicitacao": "renovação",
    "apolice_number": "SEG-RES-2024-001122",
    "detalhes": "renovação com mesmas coberturas"
  }
}
```

---

## 💰 Caso de Uso 3: Dúvida sobre Cobertura

### Cenário
Cliente quer saber se está coberto para roubo de celular dentro do carro.

### Teste

```bash
# 1. Fazer pergunta
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Meu seguro cobre roubo de eletrônicos deixados no carro? Meu celular foi roubado!"
  }' > response.json

SESSION=$(cat response.json | jq -r '.session_id')
cat response.json | jq '.answer'

# 2. Confirmar apólice
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"APO-2024-555666\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"validacao\"
  }" | jq '.{answer, flow_category, current_stage}'

# 3. Detalhar dúvida
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"É realmente coberto? Preciso registrar um sinistro de roubo\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"informacao\"
  }" | jq '.{answer, flow_complete}'
```

---

## 📄 Caso de Uso 4: Documentação para Sinistro

### Cenário
Cliente precisa saber quais documentos são necessários para abrir um sinistro de carro.

### Teste

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quais documentos são necessários para abrir um sinistro?"
  }' | jq '.{
    question,
    answer,
    flow_category,
    faq_match
  }'
```

**Resposta Esperada (FAQ Match):**
```json
{
  "question": "Quais documentos são necessários para abrir um sinistro?",
  "answer": "São necessários documento de identificação, CNH, boletim de ocorrência (quando aplicável), apólice do seguro e fotos do dano.",
  "flow_category": "documentos",
  "faq_match": true
}
```

---

## 💳 Caso de Uso 5: Parcelamento de Pagamento

### Cenário
Cliente quer parcelar o pagamento de sua apólice em 12 vezes.

### Teste

```bash
# 1. Pergunta inicial
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Posso parcelar meu boleto em mais vezes?"}' | jq '.{
    answer,
    session_id,
    flow_category,
    current_stage
  }' > flow_data.json

SESSION=$(cat flow_data.json | jq -r '.session_id')

# 2. Selecionar método
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Prefiro parcelar em 12 vezes\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"inicial\"
  }" | jq '.answer'

# 3. Validar dados
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Minha apólice é APO-PAG-2024-123456\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"validacao\"
  }" | jq '.answer'

# 4. Confirmar parcelamento
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Confirmo o parcelamento em 12x de R\$ 85,50\",
    \"session_id\": \"$SESSION\",
    \"current_stage\": \"informacao\"
  }" | jq '.{answer, flow_complete}'
```

---

## 📞 Caso de Uso 6: Suporte Geral

### Cenário
Cliente ligou para SAC e não sabe qual fluxo usar. Faz uma pergunta genérica.

### Teste

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Oi, como vocês funcionam?"
  }' | jq '.{
    answer,
    flow_category,
    current_stage,
    faq_match
  }'
```

**Resposta Esperada:**
```json
{
  "answer": "Bem-vindo! Sou um assistente de seguros. Posso ajudar com:\n- Sinistros\n- Apólices\n- Coberturas\n- Pagamentos\n- Documentos\n\nO que você precisa?",
  "flow_category": "atendimento",
  "current_stage": "inicial",
  "faq_match": false
}
```

---

## 🧪 Teste Automatizado (Script)

### Script de Testes Completos

```bash
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

API="http://localhost:8000/api/v1"
TESTS_PASSED=0
TESTS_FAILED=0

# Função para testar endpoint
test_endpoint() {
  local name=$1
  local method=$2
  local endpoint=$3
  local data=$4
  
  echo -e "${YELLOW}Testando: $name${NC}"
  
  if [ "$method" = "GET" ]; then
    response=$(curl -s -X GET "$API$endpoint")
  else
    response=$(curl -s -X POST "$API$endpoint" \
      -H "Content-Type: application/json" \
      -d "$data")
  fi
  
  # Verificar se tem 'answer' ou 'flows' ou 'session_id'
  if echo "$response" | jq . &>/dev/null; then
    if echo "$response" | jq -e '.answer or .flows or .session_id' >/dev/null 2>&1; then
      echo -e "${GREEN}✓ PASSOU${NC}\n"
      ((TESTS_PASSED++))
    else
      echo -e "${RED}✗ FALHOU - Resposta inválida${NC}\n"
      echo "$response"
      ((TESTS_FAILED++))
    fi
  else
    echo -e "${RED}✗ FALHOU - Erro JSON${NC}\n"
    echo "$response"
    ((TESTS_FAILED++))
  fi
}

# Executar testes
echo -e "${YELLOW}=== INICIANDO TESTES ===${NC}\n"

test_endpoint "Listar Fluxos" "GET" "/flows" ""

test_endpoint "Detalhes Fluxo Sinistro" "GET" "/flows/sinistro" ""

test_endpoint "Etapas Fluxo" "GET" "/flows/sinistro/stages" ""

test_endpoint "Chat Básico" "POST" "/chat" \
  '{"question": "Preciso de ajuda"}'

test_endpoint "Chat com Escalação" "POST" "/chat" \
  '{"question": "URGENTE! Meu seguro de vida é crítico!"}'

# Resultado final
echo -e "${YELLOW}=== RESULTADOS ===${NC}"
echo -e "${GREEN}Passou: $TESTS_PASSED${NC}"
echo -e "${RED}Falhou: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
  echo -e "\n${GREEN}✅ TODOS OS TESTES PASSARAM${NC}"
  exit 0
else
  echo -e "\n${RED}❌ ALGUNS TESTES FALHARAM${NC}"
  exit 1
fi
```

### Executar

```bash
chmod +x test_flows.sh
./test_flows.sh
```

---

## 🔍 Teste de Carga

### Simular Múltiplos Usuários

```bash
#!/bin/bash

# Simular 10 usuários fazendo perguntas simultâneas
for i in {1..10}; do
  (
    curl -s -X POST http://localhost:8000/api/v1/chat \
      -H "Content-Type: application/json" \
      -d "{\"question\": \"Usuário $i precisa de ajuda com sinistro\"}" \
      | jq ".session_id" > "session_$i.txt"
  ) &
done

wait
echo "✅ 10 usuários criados com sucesso"
ls session_*.txt
```

---

## ✅ Checklist de Validação

Para cada caso de uso, validar:

- [ ] Pergunta inicial detecta o fluxo correto
- [ ] Session ID é gerado e retornado
- [ ] Current_stage progride corretamente
- [ ] Next_stage é fornecido
- [ ] Resposta faz sentido contextualmente
- [ ] Flow completa quando esperado
- [ ] Escalação é detectada se necessário
- [ ] Dados coletados estão corretos
- [ ] Não há erros de validação

---

## 📊 Esperado vs Observado

| Caso | Entrada | Flow Esperado | Status |
|------|---------|---------------|--------|
| Sinistro Urgente | "URGENTE! Incêndio" | sinistro + escalação | ✅ |
| Renovação | "Renovar apólice" | apolice (4 etapas) | ✅ |
| Dúvida Cobertura | "Roubo coberto?" | cobertura (3 etapas) | ✅ |
| FAQ | "Docs necessários?" | documentos + FAQ match | ✅ |
| Pagamento | "Parcelar boleto" | pagamento (4 etapas) | ✅ |
| Suporte Geral | "Como funciona?" | atendimento (3 etapas) | ✅ |

---

## 🐛 Troubleshooting

### Problema: Fluxo não é detectado

```bash
# Teste com palavras-chave claras
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "sinistro acidente indenização"}' \
  | jq '.flow_category'
```

**Esperado**: `"sinistro"`

### Problema: Session ID não é preservado

```bash
# Verifique se está usando o mesmo session_id
SESSION=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "teste"}' | jq -r '.session_id')

echo $SESSION  # Deve imprimir UUID válido
```

### Problema: Flow não completa

```bash
# Verifique estado da sessão
curl -X GET "http://localhost:8000/api/v1/sessions/$SESSION" \
  | jq '.flow_complete, .current_stage'
```

---

**Próximo?** Consulte `FLOW_EXECUTION_GUIDE.md` para instruções detalhadas.
