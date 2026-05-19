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
| `POST` | `/api/v1/chat` | Enviar pergunta ao chatbot |
| `GET` | `/api/v1/documents` | Listar documentos carregados |
| `POST` | `/api/v1/documents/upload` | Upload de novo documento |
| `DELETE` | `/api/v1/documents/{filename}` | Remover documento |
| `GET` | `/api/v1/faq` | Listar perguntas frequentes carregadas |
| `GET` | `/api/v1/faq/categories` | Listar categorias de FAQ |

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
