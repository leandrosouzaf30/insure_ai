# ⚡ Quick Reference

Guia rápido para tarefas comuns.

---

## 🚀 Iniciar Projeto

```bash
# 1. Instalar dependências
poetry install

# 2. Configurar .env
export GOOGLE_API_KEY="sua_chave"

# 3. Rodar aplicação
poetry run uvicorn src.main:app --reload

# 4. Acessar
http://localhost:8000/docs
```

---

## 🧪 Testes

```bash
# Todos os testes
poetry run pytest tests/ -v

# Apenas fluxos
poetry run pytest tests/test_flows.py -v

# Com cobertura
poetry run pytest tests/ --cov=src
```

---

## 📂 Estrutura em Uma Linha

```
src/ (código) | docs/ (docs) | data/ (dados) | scripts/ (utilitários) | tests/ (testes)
```

---

## 📝 Imports

| Contexto | Importar |
|----------|----------|
| Dentro `src/` | `from ..config import X` |
| Fora `src/` | `from src.config import X` |
| Submodulos | `from ..rag.flows import X` |

---

## 📚 Documentação

- `docs/README.md` - Completa
- `docs/QUICK_START.md` - Início rápido
- `DEVELOPMENT.md` - Guia dev
- `REORGANIZATION_SUMMARY.md` - Mudanças

---

## 🔧 Tarefas Comuns

```bash
# Rodar tudo
poetry run uvicorn src.main:app --reload

# Linter
poetry run pylint src/

# Format
poetry run black src/

# Novo pacote
poetry add nome

# Remover pacote
poetry remove nome
```

---

**Status**: ✅ Pronto para usar
