# 🤖 Chatbot RAG com Gemini 3 Flash — FastAPI

API REST para chatbot com **Retrieval-Augmented Generation (RAG)** usando o SDK `google-genai` e o modelo **Gemini 3 Flash Preview**.

> Desenvolvido por **InsurAI Squad (Lilian e Leandro)** — Desafio 2 i2a2 Academy 2026.

---

## 🚀 Quick Start

```bash
# 1. Instalar dependências
poetry install

# 2. Configurar variáveis de ambiente
export GOOGLE_API_KEY="sua_chave"

# 3. Rodar a aplicação
poetry run uvicorn src.main:app --reload

# 4. Acessar a API
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## 📁 Estrutura do Projeto

```
insure_ai/
├── src/                          # 🔧 Código principal
│   ├── main.py                   # Aplicação FastAPI
│   ├── config.py                 # Configurações
│   ├── api/
│   │   └── routes.py             # Endpoints
│   └── rag/
│       ├── generator.py          # Geração com Gemini
│       ├── loader.py             # Carregamento de docs
│       ├── retriever.py          # Recuperação de chunks
│       ├── faq.py                # Categorização
│       └── flows.py              # Fluxos de atendimento
├── data/
│   └── documents/                # Base de conhecimento
├── docs/                         # 📚 Documentação
│   ├── README.md
│   ├── QUICK_START.md
│   ├── API_EXAMPLES.md
│   └── ...
├── scripts/                      # 🔧 Utilitários
│   ├── client.py
│   └── flows_diagram.py
├── tests/
│   └── test_flows.py
└── pyproject.toml
```

---

## 📚 Documentação Completa

Consulte a documentação detalhada em `docs/`:

- **[README.md](docs/README.md)** - Documentação completa
- **[QUICK_START.md](docs/QUICK_START.md)** - Guia de início rápido
- **[EXAMPLES_API_CALLS.md](docs/EXAMPLES_API_CALLS.md)** - Exemplos de requisições
- **[FLOWS_DOCUMENTATION.md](docs/FLOWS_DOCUMENTATION.md)** - Fluxos de atendimento
- **[IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md)** - Resumo técnico
- **[VERIFICATION_CHECKLIST.md](docs/VERIFICATION_CHECKLIST.md)** - Checklist de implementação

---

## 🎯 Recursos Principais

- ✅ 6 Fluxos de atendimento específicos
- ✅ RAG com integração de FAQs
- ✅ Detecção automática de categoria
- ✅ Rastreamento de sessão
- ✅ Escalação automática de urgências
- ✅ Modelo Gemini 3 Flash Preview
- ✅ API REST com FastAPI
- ✅ Documentação completa

---

## 🛠️ Requisitos

- Python >= 3.12
- Poetry
- Google API Key (gemini-3-flash-preview)

---

## 📞 Suporte

Para mais informações, consulte a documentação em `docs/` ou abra um issue no repositório.
