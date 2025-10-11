"""RAG operations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..config import settings
from ..db import get_db
from ..logging_utils import append_log
from ..models import Document, EmbeddingMeta
from ..security import get_current_user
from ..services import embeddings
from ..services.vector_store import VectorStore

router = APIRouter()


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            break
    return [c.strip() for c in chunks if c.strip()]


@router.post("/index", response_model=schemas.RagIndexResponse)
def index_docs(db: Session = Depends(get_db), user=Depends(get_current_user)) -> schemas.RagIndexResponse:
    """Index markdown documents under the docs directory."""

    docs_dir = Path(settings.docs_dir)
    if not docs_dir.exists():
        raise HTTPException(status_code=404, detail="Docs directory missing")
    all_chunks: List[str] = []
    meta: List[dict] = []
    documents_indexed = 0

    for path in docs_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        checksum = hashlib.sha256(text.encode("utf-8")).hexdigest()
        doc = db.query(Document).filter(Document.path == str(path)).first()
        if doc and doc.checksum == checksum:
            continue
        if not doc:
            doc = Document(path=str(path), checksum=checksum)
        else:
            doc.checksum = checksum
        db.add(doc)
        db.commit()
        db.refresh(doc)
        db.query(EmbeddingMeta).filter(EmbeddingMeta.document_id == doc.id).delete()
        db.commit()
        documents_indexed += 1
        chunks = _chunk_text(text)
        for idx, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            meta.append(
                {
                    "document_id": doc.id,
                    "chunk_id": f"{doc.id}-{idx}",
                    "path": str(path),
                    "snippet": chunk[:200],
                }
            )

    if not all_chunks:
        return schemas.RagIndexResponse(documents_indexed=0, chunks_indexed=0, backend=settings.vector_backend)

    vectors = embeddings.embed_texts(all_chunks)
    dim = vectors.shape[1]
    store = VectorStore(dim)
    store.reset()
    metadata_with_vectors = []
    for vector, info in zip(vectors, meta):
        info_with_vec = dict(info)
        info_with_vec["vector"] = vector.astype("float32").tolist()
        metadata_with_vectors.append(info_with_vec)
        embedding_meta = EmbeddingMeta(
            document_id=info["document_id"],
            chunk_id=info["chunk_id"],
            vector_backend=store.backend,
            extra=json.dumps({"path": info["path"]}),
        )
        db.add(embedding_meta)
    store.add(vectors, metadata_with_vectors)
    db.commit()
    append_log("rag_index", user=user.email, path="/rag/index", status="ok", detail=str(len(all_chunks)))
    return schemas.RagIndexResponse(
        documents_indexed=documents_indexed,
        chunks_indexed=len(all_chunks),
        backend=store.backend,
    )


@router.post("/ask", response_model=schemas.RagQueryResponse)
def ask(
    payload: schemas.RagQueryRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> schemas.RagQueryResponse:
    """Answer a question using embeddings."""

    query_vec = embeddings.embed_text(payload.query)
    dim = len(query_vec)
    store = VectorStore(dim)
    results = store.search(query_vec, top_k=payload.top_k)
    if not results:
        raise HTTPException(status_code=404, detail="No results")
    answer_parts = [meta["snippet"] for _, meta in results]
    citations = [schemas.RagCitation(path=meta["path"], snippet=meta["snippet"]) for _, meta in results]
    answer = "\n\n".join(answer_parts)
    append_log("rag_ask", user=user.email, path="/rag/ask", status="ok", detail=payload.query)
    return schemas.RagQueryResponse(answer=answer, citations=citations)
