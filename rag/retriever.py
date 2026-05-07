"""
Módulo de recuperação de contexto relevante para a pergunta do usuário.
Implementa busca simples por palavras-chave com pontuação (TF-like).
"""

from typing import List
import re


def _tokenize(text: str) -> List[str]:
    """Extrai tokens (palavras) de um texto, normalizando para minúsculas."""
    return re.findall(r"\b\w+\b", text.lower())


def _score_document(query_tokens: List[str], doc_content: str) -> float:
    """
    Calcula um score de relevância entre a query e o documento
    com base na contagem de tokens compartilhados.
    """
    doc_tokens = _tokenize(doc_content)
    doc_set = set(doc_tokens)
    matches = sum(1 for token in query_tokens if token in doc_set)
    return matches / max(len(query_tokens), 1)


def retrieve_relevant_chunks(
    query: str,
    documents: List[dict],
    top_k: int = 3,
    min_score: float = 0.05,
) -> List[dict]:
    """
    Recupera os documentos mais relevantes para a query.

    Args:
        query: Pergunta do usuário.
        documents: Lista de documentos carregados.
        top_k: Número máximo de documentos a retornar.
        min_score: Score mínimo para incluir um documento.

    Returns:
        Lista dos documentos mais relevantes com score.
    """
    if not documents:
        return []

    query_tokens = _tokenize(query)
    scored = []

    for doc in documents:
        score = _score_document(query_tokens, doc["content"])
        if score >= min_score:
            scored.append({**doc, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def build_context_from_chunks(chunks: List[dict]) -> str:
    """
    Monta o bloco de contexto a partir dos chunks recuperados.

    Args:
        chunks: Documentos relevantes com score.

    Returns:
        String formatada para injetar no prompt do LLM.
    """
    if not chunks:
        return ""

    parts = []
    for i, chunk in enumerate(chunks, 1):
        score_pct = chunk.get("score", 0) * 100
        parts.append(
            f"[Fonte {i}: {chunk['filename']} | relevância: {score_pct:.1f}%]\n"
            f"{chunk['content']}\n"
        )

    return "\n---\n".join(parts)