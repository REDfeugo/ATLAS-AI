"""Index text documents from the configured Documents directory."""

from __future__ import annotations

from pathlib import Path

from apps.api_fastapi.core.config import get_settings
from apps.api_fastapi.core.db import SessionLocal
from apps.api_fastapi.services.memory_service import MemoryService

CHUNK_SIZE = 400


def chunk_text(text: str, size: int = CHUNK_SIZE) -> list[str]:
    """Yield overlapping chunks to keep context manageable."""

    lines = text.splitlines()
    buffer: list[str] = []
    chunks: list[str] = []
    for line in lines:
        buffer.append(line)
        joined = "\n".join(buffer)
        if len(joined) >= size:
            chunks.append(joined)
            buffer = []
    if buffer:
        chunks.append("\n".join(buffer))
    return chunks


def main() -> None:
    settings = get_settings()
    if not settings.index_documents:
        print("INDEX_DOCUMENTS disabled; skipping")
        return
    documents_root = Path(settings.documents_path).expanduser()
    if not documents_root.exists():
        print(f"Documents path {documents_root} not found")
        return
    with SessionLocal() as session:
        memory = MemoryService(session)
        for path in documents_root.rglob("*.txt"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for idx, chunk in enumerate(chunk_text(text)):
                memory.upsert_document_chunk(str(path), idx, chunk)
        session.commit()
    print("Documents indexed")


if __name__ == "__main__":
    main()
