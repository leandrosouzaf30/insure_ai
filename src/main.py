"""
Ponto de entrada da aplicação FastAPI — Chatbot RAG com Gemini.
Desenvolvido por InsurAI Squad (Lilian e Leandro) — Desafio 2 i2a2 Academy 2026.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router

app = FastAPI(
    title="🤖 Chatbot RAG com Gemini",
    description=(
        "API de chatbot com Retrieval-Augmented Generation (RAG) "
        "utilizando o SDK google-genai e o modelo Gemini 3 Flash Preview.\n\n"
        "**Desenvolvido por InsurAI Squad** — Desafio 2 i2a2 Academy 2026."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — permite chamadas de frontends locais durante desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )