# 🚀 Quick Start Guide

## ✅ Implementação Concluída com Sucesso

🎯 Fluxos de Atendimento Específicos por Tipo de Consulta - v1.0 (Maio 2026)

---

## 📋 Resumo Executivo

### O que foi feito:

- ✅ Sistema completo de FLUXOS DE ATENDIMENTO CONVERSACIONAIS
- ✅ 6 fluxos específicos para: Sinistro, Apólice, Cobertura, Documentos, Pagamento, e Atendimento Geral
- ✅ Detecção automática de categoria e escalação de urgências
- ✅ Rastreamento de sessão com contexto entre mensagens
- ✅ Enriquecimento de prompt com instruções específicas do fluxo
- ✅ 5 novos endpoints para gerenciar fluxos
- ✅ 20+ testes validando funcionamento
- ✅ Documentação completa (5 arquivos, 1200+ linhas)

---

## 📊 Números

| Métrica | Valor |
|---------|-------|
| Arquivos Criados | 7 |
| Arquivos Modificados | 2 |
| Linhas de Código | 1300+ |
| Testes Implementados | 20+ |
| Documentação | 1200+ linhas |
| Endpoints Novos | 5 |
| Fluxos Implementados | 6 |
| Etapas Sequenciais | 24 |

---

## 🎯 6 Fluxos Implementados

### 🚨 Fluxo de Sinistro (Prioridade: ALTA)

**Etapas: 5**

1. Inicial: "Quando o evento ocorreu?"
2. Validação: "Qual é o número da sua apólice?"
3. Informação: "Descreva o que aconteceu"
4. Ação: "Você tem BO ou fotos?"
5. Confirmação: "Sinistro registrado"

**Detecção:** sinistro, acidente, indenização, dano  
**Escalação:** urgente, crítico, morte, incêndio, assalto  
**Tempo:** Contato em 24h

---

### 📋 Fluxo de Apólice (Prioridade: MÉDIA)

**Etapas: 4**

- Seleciona tipo de solicitação (renovação, cancelamento, etc)
- Valida número da apólice
- Coleta detalhes adicionais
- Confirma e agenda atendimento

**Detecção:** apólice, contrato, renovação, cancelamento  
**Tempo:** Confirmação em 2h úteis

---

### 📖 Fluxo de Cobertura (Prioridade: MÉDIA)

**Etapas: 4**

- Seleciona tipo de cobertura
- Valida elegibilidade
- Coleta informações específicas
- Confirma solicitação

**Detecção:** cobertura, assistência, exclusão, proteção  
**Tempo:** Confirmação em 2h

---

### 📄 Fluxo de Documentos (Prioridade: MÉDIA)

**Etapas: 3**

- Identifica documento necessário
- Coleta dados complementares
- Agenda entrega ou envio

**Detecção:** documento, comprovante, boleto, CPF  
**Tempo:** Entrega em 24h

---

### 💰 Fluxo de Pagamento (Prioridade: BAIXA)

**Etapas: 4**

- Seleciona método de pagamento
- Valida dados
- Coleta comprovação se necessário
- Confirma processamento

**Detecção:** pagamento, boleto, parcelamento, fatura  
**Tempo:** Processamento em 2h

---

### ☎️ Fluxo de Atendimento (padrão - Prioridade: BAIXA)

**Etapas: 3**

- Identifica questão
- Coleta contexto
- Fornece resposta ou agenda atendimento

**Detecção:** dúvida, suporte, ajuda, contato  
**Tempo:** Variável

---

## 🚀 Como Usar

### 1️⃣ Instalar

```bash
poetry install
```

### 2️⃣ Configurar

```bash
export GOOGLE_API_KEY="sua_chave"
```

### 3️⃣ Testar

```bash
pytest tests/test_flows.py -v          # Rodar testes
python -m docs.VERIFICATION_CHECKLIST  # Ver checklist
python scripts/flows_diagram.py        # Ver diagrama
```

### 4️⃣ Rodar

```bash
poetry run uvicorn src.main:app --reload
```

### 5️⃣ Usar

```
http://localhost:8000/docs               # Swagger
curl http://localhost:8000/api/v1/flows  # Listar fluxos
```

### 6️⃣ Exemplo

```bash
# Iniciar fluxo de sinistro
curl -X POST http://localhost:8000/api/v1/chat \
  -d '{"question":"Meu carro foi atingido"}'

# Resposta inclui:
# - session_id: para rastreamento
# - flow_category: "sinistro"
# - current_stage: "inicial"
```

---

## 📚 Próximos Passos

1. Explorar os endpoints em `/docs`
2. Revisar a documentação em `docs/`
3. Rodas os testes para validação
4. Customizar fluxos conforme necessário
