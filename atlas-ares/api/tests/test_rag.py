"""RAG endpoint tests."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import numpy as np
from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    client.post("/auth/signup", json={"email": "rag@example.com", "password": "password123"})
    resp = client.post("/auth/login", json={"email": "rag@example.com", "password": "password123"})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


class DummyStore:
    backend = "dummy"
    _storage: ClassVar[list[dict]] = []

    def __init__(self, dim: int, backend: str | None = None) -> None:  # noqa: D401 - test stub
        self.dim = dim

    def reset(self) -> None:
        DummyStore._storage = []

    def add(self, vectors: np.ndarray, metadata):
        DummyStore._storage = list(metadata)

    def search(self, query, top_k: int = 3):
        return [(0.0, meta) for meta in DummyStore._storage[:top_k]]


def test_rag_index_and_ask(client: TestClient, tmp_path: Path, monkeypatch) -> None:
    from api.routes import rag as rag_module

    headers = _auth_headers(client)
    doc_path = Path(rag_module.settings.docs_dir) / "sample.md"
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text("Atlas ARES documentation.", encoding="utf-8")

    monkeypatch.setattr(rag_module.embeddings, "embed_texts", lambda texts: np.array([[0.1, 0.2] for _ in texts]))
    monkeypatch.setattr(rag_module.embeddings, "embed_text", lambda text: np.array([0.1, 0.2]))
    monkeypatch.setattr(rag_module, "VectorStore", DummyStore)

    index_resp = client.post("/rag/index", headers=headers)
    assert index_resp.status_code == 200
    ask_resp = client.post("/rag/ask", json={"query": "Atlas"}, headers=headers)
    assert ask_resp.status_code == 200
    body = ask_resp.json()
    assert body["citations"][0]["path"].endswith("sample.md")
