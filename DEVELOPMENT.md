# 🛠️ Guia de Desenvolvimento

Este documento descreve como trabalhar com o projeto após a reorganização estrutural.

---

## 📁 Estrutura do Projeto

```
insure_ai/
├── src/                          # 🔧 Código-fonte principal (todos os módulos Python)
│   ├── __init__.py              
│   ├── main.py                   # Aplicação FastAPI (ponto de entrada)
│   ├── config.py                 # Configurações e variáveis de ambiente
│   ├── api/                      
│   │   ├── __init__.py
│   │   └── routes.py             # Endpoints da API REST
│   └── rag/                      
│       ├── __init__.py
│       ├── generator.py          # Geração de respostas com Gemini
│       ├── loader.py             # Carregamento de documentos
│       ├── retriever.py          # Recuperação de chunks relevantes
│       ├── faq.py                # Categorização de intenções/FAQs
│       └── flows.py              # Fluxos de atendimento conversacionais
│
├── data/                         # 📊 Dados e recursos
│   └── documents/
│       └── faqs.json             # Base de conhecimento estruturada
│
├── docs/                         # 📚 Documentação do projeto
│   ├── README.md                 # Documentação técnica completa
│   ├── QUICK_START.md            # Guia de início rápido
│   ├── EXAMPLES_API_CALLS.md     # Exemplos de requisições
│   ├── FLOWS_DOCUMENTATION.md    # Detalhes dos fluxos
│   ├── IMPLEMENTATION_SUMMARY.md # Resumo técnico da implementação
│   ├── FINAL_SUMMARY.md          # Sumário do projeto
│   ├── DOCUMENTATION_INDEX.md    # Índice de documentação
│   └── VERIFICATION_CHECKLIST.md # Checklist de verificação
│
├── scripts/                      # 🔧 Scripts auxiliares e utilitários
│   ├── client.py                 # Cliente para testar a API
│   └── flows_diagram.py          # Visualização dos fluxos
│
├── tests/                        # ✅ Testes unitários e integração
│   ├── __init__.py
│   └── test_flows.py             # Testes dos fluxos de atendimento
│
├── .env                          # ⚙️ Variáveis de ambiente (NÃO commitar)
├── .env.example                  # Modelo do arquivo .env
├── .gitignore
├── pyproject.toml                # Configuração do Poetry (dependências)
├── poetry.lock                   # Lock file do Poetry (versões exatas)
├── README.md                     # README principal (wrapper para docs/)
└── DEVELOPMENT.md                # Este arquivo
```

---

## 🚀 Como Rodar o Projeto

### 1. Instalação de Dependências

```bash
poetry install
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar sua chave
export GOOGLE_API_KEY="sua_chave_aqui"
```

### 3. Rodar a Aplicação

```bash
# Modo desenvolvimento (com auto-reload)
poetry run uvicorn src.main:app --reload

# Modo produção
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 4. Acessar a API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Raiz**: http://localhost:8000/

---

## 🧪 Rodando Testes

```bash
# Todos os testes
poetry run pytest tests/ -v

# Apenas testes de fluxos
poetry run pytest tests/test_flows.py -v

# Com cobertura
poetry run pytest tests/ --cov=src --cov-report=html
```

---

## 🔍 Estrutura de Imports (Importante!)

Após a reorganização, **todos os imports dentro de `src/` usam relative imports**:

### ✅ Correto (dentro de `src/`)

```python
# Em src/main.py
from .api.routes import router

# Em src/api/routes.py
from ..config import DOCS_DIR
from ..rag.loader import load_documents

# Em src/rag/generator.py
from ..config import GEMINI_MODEL
```

### ❌ Incorreto (não usar a partir de agora)

```python
# NÃO fazer isso mais:
from api.routes import router      # ❌
from config import GEMINI_MODEL    # ❌
```

### 📝 Scripts e Testes (dentro ou fora de `src/`)

```python
# Em tests/test_flows.py (fora de src/)
from src.rag.flows import FLOWS_MAP

# Em scripts/client.py (fora de src/)
# Pode usar imports absolutos se necessário
```

---

## 📝 Adicionando Novos Módulos

### Se é lógica principal (RAG, API):
```
src/
├── rag/
│   └── seu_modulo.py          # ← Coloque aqui
```

### Se é rota/endpoint:
```
src/
├── api/
│   └── novo_endpoint.py       # ← Ou estenda routes.py
```

### Se é dado/recurso:
```
data/
└── seu_recurso/               # ← Coloque aqui
    └── arquivo.json
```

### Se é utilitário/teste:
```
scripts/seu_script.py          # ← Utilitário
tests/test_seu_modulo.py       # ← Teste
```

---

## 📚 Localização da Documentação

**Toda documentação agora está em `docs/`**:

- Leia `docs/README.md` para documentação técnica completa
- Consulte `docs/QUICK_START.md` para guia de início rápido
- Veja `docs/FLOWS_DOCUMENTATION.md` para entender os fluxos
- Acesse `docs/EXAMPLES_API_CALLS.md` para exemplos de requests

---

## 🔧 Comandos Úteis

```bash
# Verificar se há erros/warnings
poetry run pylint src/

# Formatar código
poetry run black src/

# Rodar linter
poetry run flake8 src/

# Adicionar nova dependência
poetry add nome_do_pacote

# Remover dependência
poetry remove nome_do_pacote

# Atualizar dependências
poetry update
```

---

## ❓ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'src'"

**Problema**: O Python não consegue encontrar o módulo `src/`.

**Solução**: Certifique-se de:
1. Estar rodando com `poetry run` (não `python` direto)
2. Usar relative imports dentro de `src/`
3. Usar `src.` quando importar de fora

### Erro: "No module named 'config'"

**Problema**: Import antigo ainda usando caminho absoluto.

**Solução**: Atualizar para:
```python
# De fora de src/
from src.config import GOOGLE_API_KEY

# De dentro de src/
from ..config import GOOGLE_API_KEY
```

### .env não está sendo carregado

**Solução**: Verificar se:
1. O arquivo `.env` existe na raiz
2. Rodando com `poetry run`
3. Variáveis estão no formato `KEY=value`

---

## 🎯 Próximos Passos Recomendados

1. **Adicionar type hints** em todos os módulos
2. **Implementar logging** estruturado em vez de `print()`
3. **Criar camada de persistência** para sessões (BD em vez de memória)
4. **Adicionar autenticação** na API
5. **Criar CI/CD** (GitHub Actions, GitLab CI)
6. **Dockerizar** a aplicação

---

## 📞 Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feature/sua-feature`
2. Siga a estrutura de imports (relative imports em `src/`)
3. Rode os testes: `poetry run pytest`
4. Faça commit: `git commit -m "feat: descrição da mudança"`
5. Push: `git push origin feature/sua-feature`

---

## 📄 Licença

[Especifique a licença do projeto aqui]

---

**Última atualização**: Maio 2026
