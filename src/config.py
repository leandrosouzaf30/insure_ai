import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
FAQ_FILE: str = os.getenv("FAQ_FILE", "faqs.json")

# ── Modelos compatíveis com o SDK google-genai (API v1beta / 2025-2026) ──────
# O SDK legado `google-generativeai` usava nomes como "gemini-1.5-flash".
# No novo SDK `google-genai`, os nomes corretos mudaram — veja lista abaixo.
AVAILABLE_MODELS = {
    "gemini-2.5-flash-preview-05-20",   # Preview mais recente (maio 2026)
    "gemini-2.5-pro-preview-05-06",
    "gemini-2.0-flash",                  # Estável, rápido — melhor fallback
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",            # Especificado no desafio i2a2
}

GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

# Fallback usado quando o modelo principal retorna 429 ou 404.
# gemini-2.0-flash é estável e disponível na v1beta gratuitamente.
FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "gemini-3.1-flash-lite")

DOCS_DIR: str = os.getenv("DOCS_DIR", "documents")
MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "1"))
RETRY_WAIT_SECONDS: int = int(os.getenv("RETRY_WAIT_SECONDS", "20"))

if not GOOGLE_API_KEY:
    raise EnvironmentError(
        "❌ GOOGLE_API_KEY não configurada. "
        "Execute: export GOOGLE_API_KEY='sua_chave_aqui'"
    )