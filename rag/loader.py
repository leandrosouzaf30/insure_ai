"""
Módulo responsável por carregar e processar documentos locais
para uso como base de conhecimento no sistema RAG.
"""

import os
from pathlib import Path
from typing import List

from config import FAQ_FILE


def load_documents(docs_dir: str) -> List[dict]:
    """
    Carrega todos os documentos suportados de um diretório.

    Args:
        docs_dir: Caminho para o diretório com os documentos.

    Returns:
        Lista de dicionários com 'filename' e 'content'.
    """
    supported_extensions = {".txt", ".md", ".csv", ".json"}
    documents: List[dict] = []
    path = Path(docs_dir)

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Diretório '{docs_dir}' criado. Adicione documentos lá.")
        return documents

    for file_path in sorted(path.rglob("*")):
        if (
            file_path.is_file()
            and file_path.suffix.lower() in supported_extensions
            and file_path.name != FAQ_FILE
        ):
            try:
                content = file_path.read_text(encoding="utf-8")
                if content.strip():
                    documents.append(
                        {
                            "filename": file_path.name,
                            "path": str(file_path),
                            "content": content,
                            "size": len(content),
                        }
                    )
                    print(f"✅ Carregado: {file_path.name} ({len(content)} chars)")
            except Exception as e:
                print(f"⚠️  Erro ao ler '{file_path.name}': {e}")

    return documents


def build_knowledge_base(documents: List[dict]) -> str:
    """
    Concatena todos os documentos num único bloco de contexto.

    Args:
        documents: Lista de documentos carregados.

    Returns:
        String com todo o conteúdo formatado para o contexto.
    """
    if not documents:
        return ""

    parts = []
    for doc in documents:
        parts.append(
            f"=== Documento: {doc['filename']} ===\n"
            f"{doc['content']}\n"
            f"=== Fim: {doc['filename']} ===\n"
        )

    return "\n".join(parts)