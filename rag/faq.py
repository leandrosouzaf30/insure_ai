"""
Módulo de FAQ e mapeamento de intenções para o chatbot de seguros.
"""

import csv
import json
import re
from pathlib import Path
from typing import List, Optional

CATEGORY_KEYWORDS = {
    "sinistro": ["sinistro", "acidente", "ocorrência", "indenização", "seguro de vida"],
    "apolice": ["apólice", "contrato", "vencimento", "renovação", "cancelamento"],
    "cobertura": ["cobertura", "assistência", "risco", "proteção", "incluso"],
    "documentos": ["documento", "comprovante", "carteira", "rg", "cpf", "apólice"],
    "pagamento": ["pagamento", "boleto", "fatura", "parcelamento", "vencimento"],
    "atendimento": ["contato", "telefone", "e-mail", "suporte", "ajuda", "atendimento"],
}

DEFAULT_CATEGORY = "outros"


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


def _score_text_overlap(source: str, target: str) -> float:
    source_tokens = set(_tokenize(source))
    target_tokens = set(_tokenize(target))
    if not source_tokens or not target_tokens:
        return 0.0
    intersection = source_tokens.intersection(target_tokens)
    return len(intersection) / max(len(source_tokens), len(target_tokens))


def categorize_question(question: str) -> str:
    question_lower = question.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in question_lower for keyword in keywords):
            return category
    return DEFAULT_CATEGORY


def load_faqs(docs_dir: str, filename: str = "faqs.json") -> List[dict]:
    path = Path(docs_dir) / filename
    faqs: List[dict] = []

    if path.exists():
        try:
            if path.suffix.lower() == ".json":
                with path.open("r", encoding="utf-8") as f:
                    faqs = json.load(f)
            elif path.suffix.lower() == ".csv":
                with path.open("r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    faqs = [dict(row) for row in reader]
        except Exception as e:
            print(f"⚠️  Falha ao carregar FAQ '{path.name}': {e}")

    if not faqs:
        alternative = Path(docs_dir) / "faqs.csv"
        if alternative.exists():
            return load_faqs(docs_dir, filename="faqs.csv")

    normalized: List[dict] = []
    for item in faqs:
        if not item.get("question") or not item.get("answer"):
            continue
        raw_tags = item.get("tags", [])
        if isinstance(raw_tags, str):
            tags = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]
        elif isinstance(raw_tags, list):
            tags = [str(tag).strip() for tag in raw_tags if str(tag).strip()]
        else:
            tags = []

        normalized.append(
            {
                "question": item["question"].strip(),
                "answer": item["answer"].strip(),
                "category": item.get("category", categorize_question(item["question"])),
                "tags": tags,
                "source": item.get("source", "FAQ de Seguros"),
            }
        )

    return normalized


def find_best_faq_answer(question: str, faqs: List[dict], min_score: float = 0.25) -> Optional[dict]:
    if not question or not faqs:
        return None

    best = None
    best_score = 0.0
    for faq in faqs:
        score = _score_text_overlap(question, faq["question"])
        if score > best_score:
            best = faq.copy()
            best_score = score

    if best and best_score >= min_score:
        best["score"] = best_score
        return best
    return None


def summarize_faq_categories(faqs: List[dict]) -> List[str]:
    return sorted({faq.get("category", DEFAULT_CATEGORY) for faq in faqs})


def format_faq_context(faq_item: dict) -> str:
    return (
        f"Pergunta frequente: {faq_item['question']}\n"
        f"Resposta sugerida: {faq_item['answer']}\n"
        f"Categoria: {faq_item['category']}\n"
        f"Fonte: {faq_item.get('source', 'FAQ de Seguros')}"
    )
