"""
Documentação dos Fluxos de Atendimento Conversacionais

Este módulo implementa fluxos de atendimento específicos por tipo de consulta,
possibilitando um atendimento mais estruturado, contextualizado e eficiente.
"""

# 📋 FLUXOS DE ATENDIMENTO IMPLEMENTADOS

## 1. **FLUXO DE SINISTRO** (Prioridade: ALTA)
   
   **Categorias detectadas:** "sinistro", "acidente", "ocorrência", "indenização", "dano"
   
   **Etapas do fluxo:**
   1. ✅ **Inicial**: "Quando o evento ocorreu?"
   2. 📋 **Validação**: "Qual é o número da sua apólice?"
   3. 📝 **Informação**: "Descreva o que aconteceu"
   4. 📎 **Ação**: "Você tem BO ou fotos do dano?"
   5. ✔️ **Confirmação**: Sinistro registrado com referência
   
   **Escalação automática para:** urgente, crítico, morte, incêndio, assalto
   **Tempo de resposta:** Priorizado - contato dentro de 24h
   
   ---

## 2. **FLUXO DE APÓLICE** (Prioridade: MÉDIA)
   
   **Categorias detectadas:** "apólice", "contrato", "vencimento", "renovação", "cancelamento"
   
   **Etapas do fluxo:**
   1. ✅ **Inicial**: "Como posso ajudar com sua apólice?"
   2. 📋 **Validação**: "Qual é o número da sua apólice?"
   3. 📝 **Informação**: "Detalhe melhor sua solicitação"
   4. ✔️ **Confirmação**: Solicitação registrada - confirmação por e-mail em 2h
   
   **Exemplos de consultas:** Renovação, cancelamento, alteração de dados
   **Tempo de resposta:** Normal - até 2 horas úteis
   
   ---

## 3. **FLUXO DE COBERTURA** (Prioridade: MÉDIA)
   
   **Categorias detectadas:** "cobertura", "assistência", "proteção", "risco", "incluso", "exclusão"
   
   **Etapas do fluxo:**
   1. ✅ **Inicial**: "Qual tipo de cobertura você deseja consultar?"
   2. 📋 **Validação**: "Qual é o número da sua apólice?"
   3. 📝 **Informação**: "Descreva sua dúvida sobre cobertura"
   4. ✔️ **Conclusão**: Acesso ao portal do cliente para detalhes
   
   **Exemplos de consultas:** O que está coberto? Há exclusões? Qual o limite?
   **Tempo de resposta:** Imediato ou até 2h
   
   ---

## 4. **FLUXO DE DOCUMENTOS** (Prioridade: MÉDIA)
   
   **Categorias detectadas:** "documento", "comprovante", "carteira", "rg", "cpf", "apólice", "boleto"
   
   **Etapas do fluxo:**
   1. ✅ **Inicial**: "Qual documento você precisa?"
   2. 📋 **Validação**: "Qual é seu e-mail para envio?"
   3. ✔️ **Confirmação**: Documento será enviado em até 24h
   
   **Documentos disponíveis:** Apólice, comprovante de pagamento, 2ª via de boleto, comprovante de sinistro
   **Tempo de resposta:** Até 24 horas
   
   ---

## 5. **FLUXO DE PAGAMENTO** (Prioridade: BAIXA)
   
   **Categorias detectadas:** "pagamento", "boleto", "fatura", "parcelamento", "vencimento", "débito"
   
   **Etapas do fluxo:**
   1. ✅ **Inicial**: "Como posso ajudar com seu pagamento?"
   2. 📋 **Validação**: "Qual é o número da sua apólice ou CPF?"
   3. 📝 **Informação**: "Qual é sua dúvida específica?"
   4. ✔️ **Confirmação**: Oferece opções de parcelamento ou 2ª via
   
   **Exemplos de consultas:** Boleto vencido, parcelamento, segunda via
   **Tempo de resposta:** Normal - até 2h
   
   ---

## 6. **FLUXO DE ATENDIMENTO GERAL** (Prioridade: BAIXA - Fluxo padrão)
   
   **Categorias detectadas:** "contato", "telefone", "e-mail", "suporte", "ajuda", "dúvida"
   
   **Etapas do fluxo:**
   1. ✅ **Inicial**: "Olá! Como posso ajudá-lo?"
   2. 📝 **Informação**: "Me detalhe sua solicitação"
   3. ✔️ **Conclusão**: Direciona para o fluxo correto ou oferece contatos
   
   **Usar quando:** Consulta não se encaixa em categorias específicas
   **Tempo de resposta:** Normal ou escalonamento
   
   ---

# 🔄 COMO OS FLUXOS FUNCIONAM

## Fluxo de Execução da API

```
1. Usuário envia pergunta → POST /api/v1/chat
   ↓
2. Sistema categoriza a pergunta (usando keywords)
   ↓
3. Sistema seleciona fluxo apropriado (Sinistro, Apólice, etc.)
   ↓
4. Sistema cria/recupera sessão com session_id
   ↓
5. Sistema verifica se requer escalação automática
   ↓
6. Sistema recupera contexto (FAQs + documentos)
   ↓
7. Sistema enriquece prompt com informações do fluxo
   ↓
8. Gemini gera resposta considerando:
   - Etapa atual do fluxo
   - Contexto específico da categoria
   - Informações já coletadas
   ↓
9. Sistema rastreia progresso (próxima etapa)
   ↓
10. Resposta retorna com: session_id, flow_category, current_stage, next_stage, requires_escalation
```

## Ciclo de Vida de uma Sessão

```
NOVA SESSÃO
    ↓
[session_id gerado automaticamente]
    ↓
Pergunta 1 → Detecta categoria → Inicia fluxo → stage = "inicial"
    ↓
Pergunta 2 → Continua fluxo → stage = "validacao"
    ↓
Pergunta 3 → Avança → stage = "informacao"
    ↓
Pergunta 4 → Próxima → stage = "acao"
    ↓
Pergunta 5 → Finaliza → stage = "concluido"
    ↓
/sessions/{session_id}/reset → Volta ao estado inicial
```

---

# 🔌 ENDPOINTS DE FLUXOS NA API

## Listar Fluxos Disponíveis
```bash
GET /api/v1/flows

Response:
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

## Detalhar Fluxo Específico
```bash
GET /api/v1/flows/{category}

Exemplo: GET /api/v1/flows/sinistro

Response:
{
  "category": "sinistro",
  "name": "Fluxo de Sinistro",
  "priority": 1,
  "stages_count": 5,
  "requires_escalation_keywords": ["urgente", "crítico", "morte", "incêndio", "assalto"],
  "description": "Você está sendo atendido em um fluxo prioritário de sinistro..."
}
```

## Listar Estágios de um Fluxo
```bash
GET /api/v1/flows/{category}/stages

Exemplo: GET /api/v1/flows/sinistro/stages

Response:
{
  "category": "sinistro",
  "flow_name": "Fluxo de Sinistro",
  "total_stages": 5,
  "stages": [
    {
      "step": 1,
      "stage": "inicial",
      "question": "Entendi que você precisa registrar um sinistro. Quando o evento ocorreu?",
      "required_info": ["data", "local"]
    },
    ...
  ]
}
```

## Enviar Pergunta com Fluxo
```bash
POST /api/v1/chat

Request:
{
  "question": "Meu carro foi atingido e preciso fazer um sinistro urgente!",
  "session_id": "optional-uuid",           # Omita para criar nova sessão
  "current_stage": "inicial",              # Estágio atual (default: "inicial")
  "top_k": 3,
  "model": "gemini-3-flash-preview"
}

Response:
{
  "question": "Meu carro foi atingido e preciso fazer um sinistro urgente!",
  "answer": "... resposta empática e estruturada ...",
  "session_id": "abc-123-def",
  "flow_category": "sinistro",
  "current_stage": "inicial",
  "next_stage": "validacao",
  "flow_complete": false,
  "requires_escalation": true,
  "model_used": "gemini-3-flash-preview",
  "sources": ["faqs.json"],
  "intent": "sinistro",
  "faq_match": true,
  "retries": 0,
  "error": null
}
```

## Obter Informações da Sessão
```bash
GET /api/v1/sessions/{session_id}

Response:
{
  "session_id": "abc-123-def",
  "category": "sinistro",
  "current_stage": "validacao",
  "flow_name": "Fluxo de Sinistro",
  "info_collected": {
    "data": "21/05/2026",
    "local": "São Paulo"
  }
}
```

## Resetar Sessão
```bash
POST /api/v1/sessions/{session_id}/reset

Response:
{
  "message": "✅ Sessão 'abc-123-def' resetada com sucesso!"
}
```

---

# 💡 EXEMPLOS DE USO

## Exemplo 1: Novo Sinistro (Fluxo Completo)

**Pergunta 1:**
```json
{
  "question": "Preciso registrar um sinistro. Meu carro foi atingido em um acidente."
}
```
→ `session_id: "sess-001"` criado automaticamente  
→ `flow_category: "sinistro"` detectado  
→ `current_stage: "inicial"` → `next_stage: "validacao"`

**Resposta 1:**
```
Entendido. Lamento pelo ocorrido.
Quando exatamente o acidente aconteceu? (data e local)

[Referência: #SIN-001]
```

---

**Pergunta 2:**
```json
{
  "question": "Foi ontem, 20 de maio, no bairro da Vila Mariana em São Paulo.",
  "session_id": "sess-001",
  "current_stage": "validacao"
}
```
→ `current_stage: "validacao"` → `next_stage: "informacao"`

**Resposta 2:**
```
Obrigado. Agora preciso do número da sua apólice para validar a cobertura.
```

---

## Exemplo 2: Dúvida sobre Cobertura (Fluxo Rápido)

**Pergunta 1:**
```json
{
  "question": "O seguro cobre roubo de peças?"
}
```
→ `flow_category: "cobertura"` detectado  
→ `session_id: "sess-002"` criado

**Resposta 1:**
```
A cobertura depende do plano contratado. 
Qual é o número da sua apólice para eu verificar os detalhes específicos?

[Planos comuns cobrem: roubo total, parcial, e vidros]
```

---

# ⚙️ CONFIGURAÇÃO E CUSTOMIZAÇÃO

## Adicionar Nova Categoria de Fluxo

Edite `rag/flows.py`:

```python
FLOW_NOVA_CATEGORIA = AttendanceFlow(
    category="nova_categoria",
    name="Fluxo de Nova Categoria",
    priority=2,  # 1 = urgente, 3 = baixa
    stages=[
        {
            "stage": FlowStage.INITIAL.value,
            "question": "Qual é sua pergunta?",
            "required_info": ["info1"],
        },
        # ... mais etapas
    ],
    validation_keywords=["palavra-chave1", "palavra-chave2"],
    requires_escalation_keywords=["crítico", "urgente"],
    context_prompt="Contexto específico para o LLM...",
)

# Adicione ao mapa
FLOWS_MAP["nova_categoria"] = FLOW_NOVA_CATEGORIA
```

## Modificar Palavras-Chave de Detecção

Em `rag/faq.py`, atualize `CATEGORY_KEYWORDS`:

```python
CATEGORY_KEYWORDS = {
    "sinistro": ["sinistro", "acidente", "ocorrência", "indenização", "seguro de vida", "sua_nova_palavra"],
    ...
}
```

---

# 📊 MÉTRICAS E MONITORAMENTO

Para rastrear efetividade dos fluxos, monitore:

- **Taxas de conclusão por fluxo** (quantos atingem "concluido")
- **Tempo médio por etapa**
- **Taxa de escalação** (quantos foram escalonados)
- **Satisfação do usuário** (feedback após conclusão)

---

# 🚀 PRÓXIMAS EVOLUÇÕES

- [ ] Integração com banco de dados para persistência de sessões
- [ ] Histórico de interações para treinamento futuro
- [ ] Análise de sentimento para escalação dinâmica
- [ ] Feedback do usuário após conclusão do fluxo
- [ ] Métricas e dashboard de efetividade
- [ ] Integração com CRM para consulta de dados do cliente
- [ ] Fluxos com branches condicionais (ramificações)
- [ ] Multi-idioma para fluxos
