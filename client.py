import os
from google import genai
from google.genai import types

# Inicializa o cliente
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
model_id = os.environ.get("GEMINI_MODEL")

def simples_rag(pergunta, contexto_arquivo):
    """
    Simula um RAG passando o conteúdo do arquivo 
    diretamente no prompt (Context Stuffing).
    """
    try:
        # Lendo o conteúdo do seu guia ou documento local
        with open(contexto_arquivo, 'r', encoding='utf-8') as f:
            conteudo_extra = f.read()

        # Montando o prompt com o contexto
        prompt = f"""
        Use o CONTEÚDO abaixo para responder à PERGUNTA do usuário.
        Se a informação não estiver no texto, diga que não sabe.

        CONTEÚDO:
        {conteudo_extra}

        PERGUNTA:
        {pergunta}
        """

        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Erro ao processar: {e}"

# Exemplo de uso
if __name__ == "__main__":
    # Crie um arquivo chamado 'conhecimento.txt' com algumas informações
    print(simples_rag("Qual o resumo do documento?", "documents/conhecimento.txt"))
    pass