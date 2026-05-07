"""
Módulo de geração de respostas usando o SDK google-genai.
Inclui tratamento robusto dos erros 429 RESOURCE_EXHAUSTED e 404 NOT_FOUND,
além de fallback automático para modelo estável.

Compatível com: google-genai >= 1.0.0 (API v1beta, padrão 2026)
"""

import time
from typing import Optional
from google import genai
from google.genai import types as genai_types
from google.genai import errors as genai_errors

from config import GOOGLE_API_KEY, GEMINI_MODEL, FALLBACK_MODEL, MAX_RETRIES, RETRY_WAIT_SECONDS


# Inicializa o cliente uma única vez (singleton)
_client: Optional[genai.Client] = None


def get_client() -> genai.Client:
    """Retorna o cliente Gemini, criando-o se necessário."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client


SYSTEM_PROMPT = """Você é um assistente inteligente com acesso a uma base de conhecimento.
Responda sempre em português do Brasil, de forma clara e objetiva.
Quando a informação estiver na base de conhecimento fornecida, use-a para embasar sua resposta.
Se a informação não estiver disponível na base, diga claramente e ofereça o que sabe.
Nunca invente informações."""


def build_rag_prompt(question: str, context: str) -> str:
    if context:
        return (
            f"BASE DE CONHECIMENTO:\n"
            f"{context}\n\n"
            f"Com base nas informações acima, responda:\n"
            f"PERGUNTA: {question}"
        )
    return f"PERGUNTA: {question}"


def generate_response(
    question: str,
    context: str = "",
    model: Optional[str] = None,
    use_fallback: bool = True,
) -> dict:
    client = get_client()
    selected_model = model or GEMINI_MODEL
    prompt = build_rag_prompt(question, context)
    retries = 0
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=selected_model,
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=2048,
                ),
            )
            answer = response.text or "Sem resposta gerada."
            return {
                "answer": answer,
                "model_used": selected_model,
                "retries": attempt,
                "error": None,
            }

        except genai_errors.ClientError as e:
            last_error = str(e)
            error_str = str(e)

            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait = RETRY_WAIT_SECONDS * (attempt + 1)
                print(f"⏳ [Tentativa {attempt + 1}/{MAX_RETRIES}] Quota excedida. Aguardando {wait}s...")
                time.sleep(wait)
                retries += 1

            elif "404" in error_str or "NOT_FOUND" in error_str:
                print(
                    f"❌ Modelo '{selected_model}' não encontrado na API v1beta. "
                    f"Modelos válidos: gemini-2.0-flash, gemini-2.5-flash-preview-05-20, etc."
                )
                break

            else:
                print(f"❌ Erro do cliente Gemini [{attempt + 1}/{MAX_RETRIES}]: {e}")
                break

        except Exception as e:
            last_error = str(e)
            print(f"❌ Erro inesperado: {e}")
            break

    if use_fallback and selected_model != FALLBACK_MODEL:
        print(f"🔄 Ativando fallback → modelo: {FALLBACK_MODEL}")
        return generate_response(
            question=question,
            context=context,
            model=FALLBACK_MODEL,
            use_fallback=False,
        )

    return {
        "answer": "Não foi possível gerar uma resposta. Verifique os logs.",
        "model_used": selected_model,
        "retries": retries,
        "error": last_error,
    }