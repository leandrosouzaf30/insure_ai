# 🤖 Chatbot RAG com Gemini 3 Flash

Este projeto consiste num Chatbot com capacidades de **RAG (Retrieval-Augmented Generation)** utilizando o SDK mais recente do Google Generative AI e o modelo de última geração **Gemini 3 Flash Preview**.

## 🚀 O que foi feito
1.  **Migração de SDK:** Atualização da biblioteca legada `google-generativeai` para a nova e performática `google-genai` (Padrão 2026).
2.  **Configuração de Ambiente:** Estruturação de variáveis de ambiente para gerenciar chaves de API e seleção dinâmica de modelos.
3.  **Tratamento de Erros:** Implementação de lógica para lidar com o erro `429 Resource Exhausted` e limites de cota da camada gratuita/preview.
4.  **Lógica de RAG Simples:** Criação de um sistema que utiliza a ampla janela de contexto do Gemini para processar documentos locais como base de conhecimento.

---

## 🛠️ Requisitos

* **Python 3.12+**
* **Google API Key** (Obtida no [Google AI Studio](https://aistudio.google.com/))

### Instalação das Dependências
```bash
pip install -U google-genai
```

### Configuração das Variáveis de Ambiente
Para que o projeto funcione, exporte as seguintes variáveis no seu terminal ou adicione ao seu arquivo .bashrc / .env:

```bash
# Sua chave de API do Google
export GOOGLE_API_KEY="sua_chave_aqui"
# Modelo utilizado (Preview de última geração)
export GEMINI_MODEL="gemini-3-flash-preview"
```

### ⚙️ Configuração das Variáveis de Ambiente
Para que o projeto funcione, exporte as seguintes variáveis no seu terminal ou adicione ao seu arquivo .bashrc / .env:

```bash
# Sua chave de API do Google
export GOOGLE_API_KEY="sua_chave_aqui"

# Modelo utilizado (Preview de última geração)
export GEMINI_MODEL="gemini-3-flash-preview"
```

### ⚠️ Notas sobre Limites de Uso (Quota)
Como estamos a utilizar o modelo Gemini 3 Flash Preview, é comum encontrar o erro 429 RESOURCE_EXHAUSTED.

Causa: O modelo está em fase de pré-lançamento e possui limites de requisições por minuto (RPM) reduzidos.

Solução: Se o erro persistir, aguarde 60 segundos entre as execuções ou altere a variável GEMINI_MODEL para gemini-1.5-flash para testes de desenvolvimento contínuo.

#### Desenvolvido por InsurAI Squad (Lilian e Leandro) - Desafio 2 i2a2 academy 2026.