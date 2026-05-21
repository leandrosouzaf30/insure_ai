"""
Diagrama Visual dos Fluxos de Atendimento

Visualização da estrutura e funcionamento dos fluxos conversacionais.
"""

# ────────────────────────────────────────────────────────────────────────────

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           🎯 FLUXOS DE ATENDIMENTO ESPECÍFICOS POR TIPO DE CONSULTA       ║
║                    Chatbot RAG com Gemini 3 Flash                         ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ FLUXO DE SINISTRO (Prioridade: ALTA ⚠️ 1) ──────────────────────────────┐
│                                                                            │
│  Pergunta                                                                  │
│    ↓                                                                       │
│  [Detecta: "sinistro", "acidente", "indenização"]                         │
│    ↓                                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ESTÁGIO 1: INICIAL                                                 │  │
│  │ "Quando o evento ocorreu?" → Coleta data, local                   │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ESTÁGIO 2: VALIDAÇÃO                                              │  │
│  │ "Qual é o número da sua apólice?" → Valida cobertura             │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                       │
│  ⚡ VERIFICA ESCALAÇÃO: "urgente", "crítico", "morte", "incêndio"       │
│    ↓                                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ESTÁGIO 3: INFORMAÇÃO                                             │  │
│  │ "Descreva o que aconteceu" → Coleta detalhes                     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ESTÁGIO 4: AÇÃO                                                   │  │
│  │ "Você tem BO ou fotos?" → Coleta documentos                      │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ESTÁGIO 5: CONFIRMAÇÃO                                            │  │
│  │ "Sinistro registrado #SIN-{timestamp}"                           │  │
│  │ ⏰ Contato em até 24h                                            │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


┌─ FLUXO DE APÓLICE (Prioridade: MÉDIA ⚠️ 2) ────────────────────────────┐
│                                                                          │
│  Pergunta ("Como renovo minha apólice?")                               │
│    ↓                                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ INICIAL: "Como posso ajudar com sua apólice?"                  │  │
│  │ → Identifica tipo: renovação, cancelamento, alteração          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ VALIDAÇÃO: "Qual é o número da sua apólice?"                   │  │
│  │ → Valida dados da apólice                                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ INFORMAÇÃO: "Detalhe sua solicitação"                          │  │
│  │ → Coleta contexto adicional                                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ CONFIRMAÇÃO: "Solicitação registrada"                          │  │
│  │ ⏰ Confirmação por e-mail em até 2h úteis                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘


┌─ FLUXO DE COBERTURA (Prioridade: MÉDIA ⚠️ 2) ─────────────────────────┐
│                                                                        │
│  Pergunta ("O que está coberto?")                                    │
│    ↓                                                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ INICIAL: Identifica tipo de cobertura procurada               │  │
│  │ (material, pessoal, assistência)                             │  │
│  └────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ VALIDAÇÃO: Solicita número da apólice                        │  │
│  └────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ INFORMAÇÃO: Detalha dúvida sobre cobertura                   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│    ↓                                                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ CONCLUSÃO: Direciona para portal ou especialista            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘


┌─ FLUXO DE DOCUMENTOS (Prioridade: MÉDIA ⚠️ 2) ──────────────────────┐
│                                                                      │
│  Pergunta ("Preciso de uma 2ª via de boleto")                      │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ INICIAL: Qual documento?                                   │  │
│  │ (apólice, comprovante, boleto, etc.)                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ VALIDAÇÃO: Coleta e-mail ou telefone para envio            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ CONFIRMAÇÃO: Documento será enviado em até 24h            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘


┌─ FLUXO DE PAGAMENTO (Prioridade: BAIXA ℹ️ 3) ──────────────────────┐
│                                                                      │
│  Pergunta ("Meu boleto venceu")                                    │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ INICIAL: "Como posso ajudar com seu pagamento?"            │  │
│  │ → Identifica: boleto vencido, parcelamento, etc.           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ VALIDAÇÃO: Coleta apólice ou CPF                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ INFORMAÇÃO: Detalha a dúvida                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│    ↓                                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ CONFIRMAÇÃO: Oferece opções (2ª via, parcelamento, etc)  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘


╔════════════════════════════════════════════════════════════════════════════╗
║                          📊 ARQUITETURA DO SISTEMA                         ║
╚════════════════════════════════════════════════════════════════════════════╝

                                   USUÁRIO
                                     ↓
                            [POST] /api/v1/chat
                                     ↓
                            ┌────────────────┐
                            │ Criar/Recuperar│
                            │   Session ID   │
                            └────────────────┘
                                     ↓
                            ┌────────────────┐
                            │ Categorizar    │
                            │  Pergunta      │
                            └────────────────┘
                                     ↓
                    ┌─────────────────────────────────┐
                    │  Selecionar Fluxo Apropriado    │
                    │  (Sinistro, Apólice, etc.)      │
                    └─────────────────────────────────┘
                                     ↓
                    ┌─────────────────────────────────┐
                    │  Carregar FAQs Estruturadas     │
                    │  + Documentos da Base           │
                    └─────────────────────────────────┘
                                     ↓
                    ┌─────────────────────────────────┐
                    │  Verificar Escalação Automática │
                    │  (urgente, crítico, etc.)       │
                    └─────────────────────────────────┘
                                     ↓
                    ┌─────────────────────────────────┐
                    │  Enriquecer Prompt com:         │
                    │  - Contexto do Fluxo            │
                    │  - FAQs Relevantes              │
                    │  - Documentos Recuperados       │
                    │  - Etapa Atual                  │
                    └─────────────────────────────────┘
                                     ↓
                    ┌─────────────────────────────────┐
                    │  Gerar Resposta com Gemini      │
                    │  (com fallback automático)      │
                    └─────────────────────────────────┘
                                     ↓
                    ┌─────────────────────────────────┐
                    │  Rastrear Progresso no Fluxo    │
                    │  (próxima etapa)                │
                    └─────────────────────────────────┘
                                     ↓
                            ┌────────────────┐
                            │  Retornar      │
                            │  Response JSON │
                            │  (com fluxo)   │
                            └────────────────┘
                                     ↓
                                   USUÁRIO


╔════════════════════════════════════════════════════════════════════════════╗
║                      ✅ FUNCIONALIDADES IMPLEMENTADAS                      ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ 1. FLUXOS ESTRUTURADOS
   • 6 fluxos específicos por tipo de consulta
   • Cada fluxo tem 3-5 etapas sequenciais
   • Priorização automática (ALTA, MÉDIA, BAIXA)

✅ 2. RASTREAMENTO DE SESSÃO
   • UUID único por conversa
   • Contexto mantido entre perguntas
   • Histórico de etapas completadas

✅ 3. DETECÇÃO INTELIGENTE
   • Categorização automática por palavras-chave
   • Escalonamento automático para problemas urgentes
   • Roteamento para fluxo apropriado

✅ 4. CONTEXT ENRICHMENT
   • Prompt enriquecido com instruções do fluxo
   • Orientações específicas para o Gemini
   • Coleta de informações estruturada

✅ 5. INTEGRAÇÃO COM FAQS E RAG
   • FAQs estruturadas por categoria
   • Busca semântica com relevância
   • Priorização de FAQ vs. Gemini

✅ 6. ENDPOINTS ADICIONAIS
   • GET /api/v1/flows → Listar fluxos
   • GET /api/v1/flows/{category} → Detalhar fluxo
   • GET /api/v1/flows/{category}/stages → Ver etapas
   • GET /api/v1/sessions/{session_id} → Info da sessão
   • POST /api/v1/sessions/{session_id}/reset → Resetar

✅ 7. TESTES UNITÁRIOS
   • 30+ testes para validar fluxos
   • Cobertura de casos normais e extremos
   • Validação de estrutura e progresso


╔════════════════════════════════════════════════════════════════════════════╗
║                       🚀 COMO USAR OS FLUXOS                              ║
╚════════════════════════════════════════════════════════════════════════════╝

1. INICIAR UMA CONVERSA (Nova Sessão)
   POST /api/v1/chat
   {
     "question": "Preciso registrar um sinistro",
     "top_k": 3
   }
   
   Resposta inclui: session_id, flow_category, current_stage, next_stage

2. CONTINUAR A CONVERSA (Mesma Sessão)
   POST /api/v1/chat
   {
     "question": "Ontem, 20 de maio, em São Paulo",
     "session_id": "abc-123-def",
     "current_stage": "validacao"
   }
   
   Sistema avança automaticamente para próxima etapa

3. CONSULTAR ESTÁGIOS DE UM FLUXO
   GET /api/v1/flows/sinistro/stages
   
   Retorna: lista de etapas, perguntas, dados requeridos

4. RESETAR SESSÃO
   POST /api/v1/sessions/abc-123-def/reset
   
   Volta ao estado inicial para novo atendimento


╔════════════════════════════════════════════════════════════════════════════╗
║                          📈 PRÓXIMAS EVOLUÇÕES                            ║
╚════════════════════════════════════════════════════════════════════════════╝

🔄 Curto Prazo (Semana 1-2):
   □ Integração com banco de dados (persistência de sessões)
   □ Histórico de interações para análise
   □ Feedback do usuário após conclusão
   □ Análise de sentimento para escalação dinâmica

🔄 Médio Prazo (Mês 1-2):
   □ Integração com CRM (buscar dados do cliente)
   □ Fluxos com branches condicionais (ramificações)
   □ Suporte multi-idioma
   □ Transferência para agente humano

🔄 Longo Prazo (Mês 3+):
   □ Fine-tuning do Gemini com dados de sinistros
   □ ML para predição de intenção
   □ Dashboard de métricas e efetividade
   □ Chatbot com suporte a múltiplos canais (WhatsApp, SMS, etc.)

""")


if __name__ == "__main__":
    print("✅ Diagrama carregado com sucesso!")
