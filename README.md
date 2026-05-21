# 🤖 Chatbot RAG com Gemini 3 Flash — FastAPI

API REST para chatbot com **Retrieval-Augmented Generation (RAG)** usando o SDK `google-genai` e o modelo **Gemini 3 Flash Preview**.

> Desenvolvido por **InsurAI Squad (Lilian e Leandro)** — Desafio 2 i2a2 Academy 2026.

---

## 📁 Estrutura do Projeto

```
.
├── api/
│   ├── __init__.py
│   └── routes.py         # Endpoints FastAPI
├── documents/            # Base de conhecimento (.txt, .md, .csv, .json), incluindo FAQs estruturadas
├── rag/
│   ├── __init__.py
│   ├── generator.py      # Geração de resposta com Gemini
│   ├── loader.py         # Carregamento de documentos
│   └── retriever.py      # Recuperação de chunks relevantes
├── .env.example          # Modelo do arquivo de ambiente
├── config.py             # Variáveis de ambiente e configurações
├── main.py               # Ponto de entrada FastAPI
├── pyproject.toml        # Configuração do Poetry
├── poetry.lock           # Versões fixas de dependências
└── README.md
```

---

## 🚀 Instalação com Poetry

### 1. Instalar o Poetry
Se ainda não tiver o Poetry instalado:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Instalar dependências do projeto

type:

```bash
poetry install
```

### 3. Ativar o ambiente virtual do Poetry

```bash
poetry shell
```

> Alternativamente, execute comandos dentro do ambiente gerenciado pelo Poetry com `poetry run`.

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite .env e insira sua GOOGLE_API_KEY
```

Ou exporte diretamente:

```bash
export GOOGLE_API_KEY="sua_chave_aqui"
export GEMINI_MODEL="gemini-3-flash-preview"
```

### 5. Iniciar o servidor

Com o ambiente do Poetry ativado:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Ou usando `poetry run`:

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📡 Endpoints

Esta API agora inclui suporte para FAQs categorizadas, fluxos de atendimento e atendimento direcionado ao segurado.

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/` | Status da API |
| `POST` | `/api/v1/chat` | Enviar pergunta ao chatbot **com fluxo de atendimento** |
| `GET` | `/api/v1/documents` | Listar documentos carregados |
| `POST` | `/api/v1/documents/upload` | Upload de novo documento |
| `DELETE` | `/api/v1/documents/{filename}` | Remover documento |
| `GET` | `/api/v1/faq` | Listar perguntas frequentes carregadas |
| `GET` | `/api/v1/faq/categories` | Listar categorias de FAQ |
| `GET` | `/api/v1/flows` | Listar fluxos de atendimento disponíveis |
| `GET` | `/api/v1/flows/{category}` | Detalhar fluxo de atendimento |
| `GET` | `/api/v1/flows/{category}/stages` | Listar estágios de um fluxo |
| `GET` | `/api/v1/sessions/{session_id}` | Obter estado da sessão de atendimento |
| `POST` | `/api/v1/sessions/{session_id}/reset` | Resetar sessão de atendimento |

---

## 🎯 Fluxos de Atendimento Específicos por Tipo de Consulta

O chatbot agora implementa **fluxos de atendimento conversacionais estruturados** que se adaptam ao tipo de consulta:

### Fluxos Disponíveis

| Fluxo | Prioridade | Etapas | Palavras-chave |
|-------|-----------|--------|----------------|
| **🚨 Sinistro** | ALTA (1) | 5 | sinistro, acidente, indenização, dano |
| **📋 Apólice** | MÉDIA (2) | 4 | apólice, contrato, renovação, cancelamento |
| **📖 Cobertura** | MÉDIA (2) | 4 | cobertura, assistência, exclusão, proteção |
| **📄 Documentos** | MÉDIA (2) | 3 | documento, comprovante, boleto, CPF |
| **💰 Pagamento** | BAIXA (3) | 4 | pagamento, boleto, parcelamento, fatura |
| **☎️ Atendimento Geral** | BAIXA (3) | 3 | dúvida, suporte, ajuda, contato |

### Como Funcionam os Fluxos

1. **Detecção Automática**: O sistema identifica o tipo de consulta e seleciona o fluxo apropriado
2. **Rastreamento de Sessão**: Cada conversa tem um `session_id` único para manter contexto
3. **Etapas Sequenciais**: O fluxo guia a coleta de informações passo a passo
4. **Escalação Inteligente**: Detecta automaticamente problemas urgentes (ex: "crítico", "morte", "incêndio")
5. **Contexto Enriquecido**: O LLM recebe instruções específicas para cada tipo de fluxo

### Exemplo de Fluxo de Sinistro

```json
// Pergunta 1: Reporte de sinistro
{
  "question": "Tive um acidente com meu carro urgente!",
  "top_k": 3
}

// Resposta 1
{
  "session_id": "abc-123-def",
  "flow_category": "sinistro",
  "current_stage": "inicial",
  "next_stage": "validacao",
  "requires_escalation": true,
  "answer": "Entendido! Lamento pelo ocorrido. Quando exatamente o acidente aconteceu?..."
}

// Pergunta 2: Continua o fluxo
{
  "question": "Ontem, 20 de maio, em São Paulo",
  "session_id": "abc-123-def",
  "current_stage": "validacao"
}

// Resposta 2
{
  "session_id": "abc-123-def",
  "flow_category": "sinistro",
  "current_stage": "validacao",
  "next_stage": "informacao",
  "answer": "Obrigado. Agora preciso do número da sua apólice..."
}
```

### Listar Fluxos Disponíveis

```bash
curl http://localhost:8000/api/v1/flows
```

```json
{
  "flows": [
    {
      "category": "sinistro",
      "name": "Fluxo de Sinistro",
      "priority": 1,
      "stages": 5,
      "description": "Você está sendo atendido em um fluxo prioritário de sinistro..."
    },
    ...
  ],
  "total_flows": 6
}
```

### Ver Estágios de um Fluxo

```bash
curl http://localhost:8000/api/v1/flows/sinistro/stages
```

**📖 Documentação completa dos fluxos:** Veja [FLOWS_DOCUMENTATION.md](FLOWS_DOCUMENTATION.md)


Documentação interativa: http://localhost:8000/docs

---

## 💬 Exemplo de uso

### Chat

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Como funciona o RAG?", "top_k": 3}'
```

### Resposta esperada

```json
{
  "question": "Como funciona o RAG?",
  "answer": "O RAG (Retrieval-Augmented Generation) funciona em três etapas...",
  "model_used": "gemini-3-flash-preview",
  "sources": ["exemplo.md"],
  "retries": 0,
  "error": null
}
```

---

## ⚠️ Tratamento de Erros 429 (RESOURCE_EXHAUSTED)

O sistema pode lidar com erros de cota retornando:

1. **Retry automático** com espera exponencial.
2. **Fallback de modelo** quando o modelo principal falha.
3. **Configurações adicionais** via `MAX_RETRIES` e `RETRY_WAIT_SECONDS`.

---

## 📄 Formatos de Documento Suportados

- `.txt` — Texto simples
- `.md` — Markdown
- `.csv` — Dados tabulares
- `.json` — Dados estruturados

Use a pasta `documents/` ou o endpoint `/api/v1/documents/upload` para adicionar novos arquivos.

