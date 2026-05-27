# 💻 Exemplos de Código: Executar Fluxos

Exemplos práticos em diferentes linguagens para executar fluxos na API.

---

## 🐍 Python

### Exemplo 1: Fluxo Completo Simples

```python
import requests
import json

# Configuração
API_BASE = "http://localhost:8000/api/v1"

# 1. Iniciar fluxo
print("📌 1. Iniciando fluxo de sinistro...")
response = requests.post(
    f"{API_BASE}/chat",
    json={"question": "Meu carro foi atingido por outro veículo"}
)

data = response.json()
session_id = data["session_id"]
print(f"Session ID: {session_id}")
print(f"Resposta: {data['answer']}\n")

# 2. Continuar fluxo
print("📌 2. Respondendo validação...")
response = requests.post(
    f"{API_BASE}/chat",
    json={
        "question": "Minha apólice é 123456789ABC",
        "session_id": session_id,
        "current_stage": "validacao"
    }
)

data = response.json()
print(f"Resposta: {data['answer']}\n")

# 3. Verificar estado
print("📌 3. Verificando estado da sessão...")
response = requests.get(f"{API_BASE}/sessions/{session_id}")
data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))
```

### Exemplo 2: Classe Reutilizável

```python
import requests
from typing import Optional, Dict, Any

class ChatbotFlowClient:
    """Cliente para interagir com fluxos de atendimento."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session_id: Optional[str] = None
    
    def list_flows(self) -> Dict[str, Any]:
        """Listar todos os fluxos disponíveis."""
        response = requests.get(f"{self.base_url}/flows")
        return response.json()
    
    def get_flow_details(self, category: str) -> Dict[str, Any]:
        """Obter detalhes de um fluxo."""
        response = requests.get(f"{self.base_url}/flows/{category}")
        return response.json()
    
    def send_message(self, question: str, current_stage: Optional[str] = None) -> Dict[str, Any]:
        """Enviar mensagem e obter resposta."""
        payload = {"question": question}
        
        if self.session_id:
            payload["session_id"] = self.session_id
        if current_stage:
            payload["current_stage"] = current_stage
        
        response = requests.post(f"{self.base_url}/chat", json=payload)
        data = response.json()
        
        # Guardar session_id
        if "session_id" in data:
            self.session_id = data["session_id"]
        
        return data
    
    def get_session_state(self) -> Dict[str, Any]:
        """Obter estado da sessão atual."""
        if not self.session_id:
            raise ValueError("Nenhuma sessão ativa")
        
        response = requests.get(f"{self.base_url}/sessions/{self.session_id}")
        return response.json()
    
    def reset_session(self) -> Dict[str, Any]:
        """Resetar sessão atual."""
        if not self.session_id:
            raise ValueError("Nenhuma sessão ativa")
        
        response = requests.post(f"{self.base_url}/sessions/{self.session_id}/reset")
        data = response.json()
        self.session_id = None
        return data

# Uso:
client = ChatbotFlowClient()

# Listar fluxos
print(client.list_flows())

# Iniciar fluxo
resp1 = client.send_message("Meu carro sofreu um acidente")
print(f"Resposta: {resp1['answer']}")

# Continuar fluxo
resp2 = client.send_message("Apólice 123456789", current_stage="validacao")
print(f"Resposta: {resp2['answer']}")

# Verificar estado
print(client.get_session_state())
```

### Exemplo 3: Com Tratamento de Erro

```python
import requests
from requests.exceptions import RequestException

def executar_fluxo_com_retry():
    """Executar fluxo com retry automático."""
    
    max_retries = 3
    retry_delay = 2  # segundos
    
    for tentativa in range(max_retries):
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/chat",
                json={"question": "Preciso de ajuda com um sinistro"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout na tentativa {tentativa + 1}")
            if tentativa < max_retries - 1:
                import time
                time.sleep(retry_delay)
        
        except requests.exceptions.ConnectionError:
            print(f"🔌 Erro de conexão na tentativa {tentativa + 1}")
            if tentativa < max_retries - 1:
                import time
                time.sleep(retry_delay)
        
        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro HTTP: {e.response.status_code}")
            print(e.response.json())
            return None
    
    print("❌ Falhou após todas as tentativas")
    return None

# Uso
resultado = executar_fluxo_com_retry()
if resultado:
    print(f"✅ Sucesso: {resultado['answer']}")
```

---

## 🟨 JavaScript/Node.js

### Exemplo 1: Fetch API

```javascript
const API_BASE = "http://localhost:8000/api/v1";

async function executarFluxo() {
  try {
    // 1. Iniciar fluxo
    console.log("📌 1. Iniciando fluxo...");
    let response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: "Meu carro foi atingido"
      })
    });
    
    let data = await response.json();
    const sessionId = data.session_id;
    console.log(`Session ID: ${sessionId}`);
    console.log(`Resposta: ${data.answer}\n`);
    
    // 2. Continuar fluxo
    console.log("📌 2. Respondendo validação...");
    response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: "Apólice 123456789ABC",
        session_id: sessionId,
        current_stage: "validacao"
      })
    });
    
    data = await response.json();
    console.log(`Resposta: ${data.answer}\n`);
    
    // 3. Verificar estado
    console.log("📌 3. Estado da sessão...");
    response = await fetch(`${API_BASE}/sessions/${sessionId}`);
    data = await response.json();
    console.log(JSON.stringify(data, null, 2));
    
  } catch (error) {
    console.error("❌ Erro:", error);
  }
}

executarFluxo();
```

### Exemplo 2: Classe com Axios

```javascript
const axios = require("axios");

class ChatbotClient {
  constructor(baseURL = "http://localhost:8000/api/v1") {
    this.baseURL = baseURL;
    this.sessionId = null;
    this.client = axios.create({ baseURL });
  }
  
  async listarFluxos() {
    const response = await this.client.get("/flows");
    return response.data;
  }
  
  async obterDetalhesFluxo(category) {
    const response = await this.client.get(`/flows/${category}`);
    return response.data;
  }
  
  async enviarMensagem(question, currentStage = null) {
    const payload = { question };
    
    if (this.sessionId) payload.session_id = this.sessionId;
    if (currentStage) payload.current_stage = currentStage;
    
    const response = await this.client.post("/chat", payload);
    const data = response.data;
    
    if (data.session_id) {
      this.sessionId = data.session_id;
    }
    
    return data;
  }
  
  async obterEstadoSessao() {
    if (!this.sessionId) throw new Error("Sem sessão ativa");
    const response = await this.client.get(`/sessions/${this.sessionId}`);
    return response.data;
  }
  
  async resetarSessao() {
    if (!this.sessionId) throw new Error("Sem sessão ativa");
    const response = await this.client.post(`/sessions/${this.sessionId}/reset`);
    this.sessionId = null;
    return response.data;
  }
}

// Uso:
(async () => {
  const client = new ChatbotClient();
  
  // Iniciar fluxo
  let resp = await client.enviarMensagem("Meu carro teve um acidente");
  console.log(`🔹 ${resp.answer}`);
  
  // Continuar
  resp = await client.enviarMensagem("Apólice 123456789", "validacao");
  console.log(`🔹 ${resp.answer}`);
  
  // Verificar estado
  const estado = await client.obterEstadoSessao();
  console.log(`✅ Fluxo completo: ${estado.flow_complete}`);
})();
```

---

## 🌐 cURL com Variáveis de Ambiente

### Script Interativo

```bash
#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

API="http://localhost:8000/api/v1"

echo -e "${BLUE}=== Chat Flow Interativo ===${NC}\n"

# Primeira mensagem
echo -e "${GREEN}Enviando pergunta inicial...${NC}"
read -p "Qual é sua pergunta? " question

RESPONSE=$(curl -s -X POST "$API/chat" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"$question\"}")

SESSION_ID=$(echo $RESPONSE | jq -r '.session_id')
ANSWER=$(echo $RESPONSE | jq -r '.answer')
STAGE=$(echo $RESPONSE | jq -r '.current_stage')

echo -e "\n${GREEN}Bot:${NC} $ANSWER"
echo -e "\n(Session: $SESSION_ID | Stage: $STAGE)"

# Loop para continuar conversa
while true; do
  read -p "\n$(echo -e ${GREEN}Você:${NC}) " user_input
  
  if [ -z "$user_input" ]; then
    continue
  fi
  
  RESPONSE=$(curl -s -X POST "$API/chat" \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"$user_input\", \"session_id\": \"$SESSION_ID\"}")
  
  ANSWER=$(echo $RESPONSE | jq -r '.answer')
  COMPLETED=$(echo $RESPONSE | jq -r '.flow_complete')
  
  echo -e "\n${GREEN}Bot:${NC} $ANSWER"
  
  if [ "$COMPLETED" = "true" ]; then
    echo -e "\n${GREEN}✅ Fluxo concluído!${NC}"
    break
  fi
done
```

---

## 📋 Fluxograma Visual de Execução

```
┌─────────────────────────────────────┐
│  1. Pergunta Inicial (Sem Session)  │
└────────────┬────────────────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ API detecta categoria  │
    │ e retorna session_id   │
    │ (ex: "sinistro")       │
    └────────────┬───────────┘
                 │
                 ▼
    ┌───────────────────────────────┐
    │ 2. Continuar com Session ID   │
    │    + current_stage            │
    │    (ex: "validacao")          │
    └────────────┬──────────────────┘
                 │
                 ▼
    ┌───────────────────────────────┐
    │ 3. Próxima Pergunta           │
    │    com mesmos dados           │
    │    (ex: "informacao")         │
    └────────────┬──────────────────┘
                 │
                 ▼
    ┌───────────────────────────────┐
    │ 4. Continuar até...           │
    │    flow_complete == true      │
    └───────────────────────────────┘
```

---

## 🎯 Padrão Recomendado

```python
def fluxo_completo(pergunta_inicial: str):
    """Padrão recomendado para executar fluxo."""
    
    # 1. Iniciar
    response = requests.post(
        "http://localhost:8000/api/v1/chat",
        json={"question": pergunta_inicial}
    )
    data = response.json()
    session_id = data["session_id"]
    
    print(f"🔹 {data['answer']}")
    
    # 2. Loop até conclusão
    while not data.get("flow_complete", False):
        # Obter entrada do usuário
        user_response = input("\nVocê: ")
        
        # Enviar com session_id
        response = requests.post(
            "http://localhost:8000/api/v1/chat",
            json={
                "question": user_response,
                "session_id": session_id,
                "current_stage": data.get("current_stage")
            }
        )
        
        data = response.json()
        
        # Mostrar resposta
        print(f"🤖 {data['answer']}")
        
        # Verificar escalação
        if data.get("requires_escalation"):
            print("⚠️ CASO ESCALADO - Será atendido com prioridade!")
    
    # 3. Resumo final
    session_state = requests.get(
        f"http://localhost:8000/api/v1/sessions/{session_id}"
    ).json()
    
    print(f"\n✅ Fluxo concluído!")
    print(f"Categoria: {session_state['flow_category']}")
    print(f"Dados coletados: {session_state['collected_info']}")
```

---

## 🔗 Integração com Frontend

### React Component

```jsx
import { useState } from 'react';

const ChatFlow = () => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const API = 'http://localhost:8000/api/v1';
  
  const sendMessage = async () => {
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: inputValue,
          session_id: sessionId
        })
      });
      
      const data = await response.json();
      
      // Guardar session_id
      setSessionId(data.session_id);
      
      // Adicionar mensagens
      setMessages([
        ...messages,
        { role: 'user', content: inputValue },
        { role: 'bot', content: data.answer }
      ]);
      
      setInputValue('');
      
    } catch (error) {
      console.error('Erro:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="chat">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      
      <input
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Digite sua pergunta..."
        disabled={isLoading}
      />
      
      <button onClick={sendMessage} disabled={isLoading}>
        Enviar
      </button>
    </div>
  );
};

export default ChatFlow;
```

---

**Próximo?** Consulte `FLOW_EXECUTION_GUIDE.md` para guia completo passo a passo.
