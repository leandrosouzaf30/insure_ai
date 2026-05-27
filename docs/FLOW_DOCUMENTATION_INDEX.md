# 📚 Índice: Executar Fluxos na API

Documentação completa sobre como executar fluxos de atendimento.

---

## 🚀 Comece Aqui

1. **Iniciante?** → [FLOW_EXECUTION_GUIDE.md](FLOW_EXECUTION_GUIDE.md)
   - Passo a passo detalhado
   - Desde iniciar a app até completar fluxos
   - Inclui erros e soluções

2. **Quer código?** → [FLOW_CODE_EXAMPLES.md](FLOW_CODE_EXAMPLES.md)
   - Python, JavaScript, cURL
   - Exemplos reutilizáveis
   - Padrões recomendados

3. **Casos reais?** → [FLOW_USE_CASES.md](FLOW_USE_CASES.md)
   - 6 cenários práticos
   - Scripts de teste
   - Checklist de validação

---

## 📊 Fluxos Disponíveis

| Fluxo | Prioridade | Etapas | Melhor Para |
|-------|-----------|--------|-----------|
| **Sinistro** | 🔴 Alta | 5 | Registrar acidentes, roubos, perdas |
| **Apólice** | 🟡 Média | 4 | Renovação, cancelamento, alterações |
| **Cobertura** | 🟡 Média | 4 | Dúvidas sobre proteção e limites |
| **Documentos** | 🟡 Média | 3 | Solicitar e validar documentos |
| **Pagamento** | 🟢 Baixa | 4 | Parcelamento, boleto, fatura |
| **Atendimento** | 🟢 Baixa | 3 | Suporte geral e dúvidas |

---

## 🎯 Fluxo de Execução Rápido

### Terminal 1: Rodar API

```bash
poetry run uvicorn src.main:app --reload
# http://localhost:8000/docs ← Swagger
```

### Terminal 2: Testar

```bash
# 1. Listar fluxos
curl http://localhost:8000/api/v1/flows

# 2. Fazer pergunta
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Meu carro foi atingido"}'

# 3. Continuar com session_id
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Apólice 123456", "session_id": "UUID", "current_stage": "validacao"}'
```

---

## 🔑 Conceitos Principais

### Session ID
- ID único gerado na primeira pergunta
- Mantém contexto entre mensagens
- Reutilizar nas próximas perguntas

### Stages (Etapas)
- `inicial` → `validacao` → `informacao` → `acao` → `confirmacao`
- Cada stage tem uma pergunta específica
- Progride automaticamente

### Escalação
- Palavras-chave urgentes disparam escalação
- Exemplo: "urgente", "crítico", "morte", "incêndio"
- Flag: `requires_escalation: true`

### Flow Complete
- `true` = Fluxo concluído com sucesso
- Dados foram coletados
- Próximo passo é análise/processamento

---

## 📝 Estrutura de Request

```json
{
  "question": "Texto da pergunta",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "current_stage": "validacao",
  "top_k": 3,
  "model": "gemini-3-flash-preview"
}
```

| Campo | Obrigatório | Tipo | Descrição |
|-------|------------|------|-----------|
| `question` | ✅ | string | Pergunta/resposta do usuário |
| `session_id` | ❌ | string | ID da sessão (usar se tiver) |
| `current_stage` | ❌ | string | Etapa atual (preenchido automaticamente) |
| `top_k` | ❌ | int | Chunks a recuperar (padrão: 3) |
| `model` | ❌ | string | Modelo Gemini (padrão: env var) |

---

## 📤 Estrutura de Response

```json
{
  "question": "Meu carro foi atingido",
  "answer": "Entendo que você precisa registrar um sinistro...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "flow_category": "sinistro",
  "current_stage": "inicial",
  "next_stage": "validacao",
  "flow_complete": false,
  "requires_escalation": false,
  "model_used": "gemini-3-flash-preview"
}
```

| Campo | Tipo | Significado |
|-------|------|-----------|
| `answer` | string | Resposta do bot para o usuário |
| `flow_category` | string | Tipo de fluxo detectado |
| `current_stage` | string | Etapa atual |
| `next_stage` | string | Próxima etapa esperada |
| `flow_complete` | boolean | Fluxo concluído? |
| `requires_escalation` | boolean | Precisa escalação? |

---

## 🧪 Endpoints Principais

```
GET  /api/v1/flows                    → Listar todos os fluxos
GET  /api/v1/flows/{category}         → Detalhes de um fluxo
GET  /api/v1/flows/{category}/stages  → Etapas do fluxo
POST /api/v1/chat                     → Enviar pergunta/continuar
GET  /api/v1/sessions/{session_id}    → Estado da sessão
POST /api/v1/sessions/{session_id}/reset → Resetar sessão
```

---

## 💡 Exemplos Rápidos

### Python

```python
import requests

# Iniciar
r = requests.post("http://localhost:8000/api/v1/chat",
  json={"question": "Preciso de um sinistro"})
session_id = r.json()["session_id"]

# Continuar
r = requests.post("http://localhost:8000/api/v1/chat",
  json={"question": "Apólice 123", "session_id": session_id})
print(r.json()["answer"])
```

### JavaScript

```javascript
const response = await fetch("http://localhost:8000/api/v1/chat", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({question: "Meu carro foi atingido"})
});
const data = await response.json();
const sessionId = data.session_id;
```

### cURL

```bash
SESSION=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -d '{"question":"Meu carro foi atingido"}' \
  | jq -r '.session_id')

curl -X POST http://localhost:8000/api/v1/chat \
  -d "{\"question\":\"Apólice 123\",\"session_id\":\"$SESSION\"}"
```

---

## 🎓 Casos de Uso

### 1️⃣ Sinistro Urgente (Incêndio)
- ⏱️ Tempo crítico
- 🚨 Escalação automática
- 📞 Contato em 30 minutos

[Veja exemplo completo →](FLOW_USE_CASES.md#-caso-de-uso-1-sinistro-urgente-incêndio)

### 2️⃣ Renovação de Apólice
- 📋 4 etapas sequenciais
- ⏰ Confirmação em 2h úteis
- 📧 Confirmação por email

[Veja exemplo completo →](FLOW_USE_CASES.md#-caso-de-uso-2-renovação-de-apólice)

### 3️⃣ Dúvida sobre Cobertura
- ❓ Perguntas sobre limites
- 📖 Consulta FAQs automaticamente
- 💬 Respostas em tempo real

[Veja exemplo completo →](FLOW_USE_CASES.md#-caso-de-uso-3-dúvida-sobre-cobertura)

### 4️⃣ Pedido de Documentos
- 📄 Validação de documentos
- ✅ Checklist automático
- 🚚 Agendamento de entrega

[Veja exemplo completo →](FLOW_USE_CASES.md#-caso-de-uso-4-documentação-para-sinistro)

### 5️⃣ Parcelamento de Pagamento
- 💳 Múltiplas opções
- 🔄 Processamento automático
- 📊 Confirmação de parcelas

[Veja exemplo completo →](FLOW_USE_CASES.md#-caso-de-uso-5-parcelamento-de-pagamento)

### 6️⃣ Suporte Geral
- 🆘 Atendimento básico
- 🔀 Redirecionamento automático
- 📚 Integração com FAQs

[Veja exemplo completo →](FLOW_USE_CASES.md#-caso-de-uso-6-suporte-geral)

---

## 📖 Documentos Completos

### [FLOW_EXECUTION_GUIDE.md](FLOW_EXECUTION_GUIDE.md)
**Para**: Iniciantes  
**Contém**:
- ⚙️ Como iniciar a aplicação
- 📋 Passo a passo completo
- 🧪 Teste de cada etapa
- ❌ Tratamento de erros
- 🔍 Dicas e boas práticas

### [FLOW_CODE_EXAMPLES.md](FLOW_CODE_EXAMPLES.md)
**Para**: Desenvolvedores  
**Contém**:
- 🐍 Python com Requests
- 🟨 JavaScript/Node.js
- 💻 cURL completo
- ⚡ Classe reutilizável
- 🔗 Integração com Frontend

### [FLOW_USE_CASES.md](FLOW_USE_CASES.md)
**Para**: Testers/QA  
**Contém**:
- 🧪 6 cenários práticos
- ✅ Teste automatizado
- 🔍 Validação de respostas
- 📊 Teste de carga
- 🐛 Troubleshooting

---

## ✅ Checklist de Setup

- [ ] Poetry instalado
- [ ] `.env` configurado com API key
- [ ] API rodando em `localhost:8000`
- [ ] Swagger acessível em `/docs`
- [ ] Consegue fazer POST em `/chat`
- [ ] Recebe `session_id` na resposta
- [ ] Consegue continuar fluxo com `session_id`
- [ ] Todos os 6 fluxos funcionam

---

## 🔗 Links Relacionados

- [docs/README.md](README.md) - Documentação técnica completa
- [docs/QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Referência rápida
- [docs/QUICK_START.md](QUICK_START.md) - Início rápido
- [../DEVELOPMENT.md](../DEVELOPMENT.md) - Guia de desenvolvimento

---

## 🎯 Próximos Passos

1. **Começar**: Leia [FLOW_EXECUTION_GUIDE.md](FLOW_EXECUTION_GUIDE.md)
2. **Codificar**: Consulte [FLOW_CODE_EXAMPLES.md](FLOW_CODE_EXAMPLES.md)
3. **Testar**: Siga [FLOW_USE_CASES.md](FLOW_USE_CASES.md)
4. **Integrar**: Use em sua aplicação

---

## 📞 Suporte

- 🐛 Erro? → Veja "Tratamento de Erros" em [FLOW_EXECUTION_GUIDE.md](FLOW_EXECUTION_GUIDE.md)
- 💬 Exemplo? → Procure em [FLOW_CODE_EXAMPLES.md](FLOW_CODE_EXAMPLES.md)
- 🧪 Teste? → Veja [FLOW_USE_CASES.md](FLOW_USE_CASES.md)

---

**Status**: ✅ Documentação Completa  
**Última Atualização**: Maio 2026
