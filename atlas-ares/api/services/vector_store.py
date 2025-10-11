"""Vector store abstraction with FAISS primary and fallbacks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence, Tuple

import numpy as np

from ..config import settings

try:  # pragma: no cover - optional dependency
    import faiss
except Exception:  # pragma: no cover
    faiss = None  # type: ignore

try:  # pragma: no cover
    from annoy import AnnoyIndex
except Exception:  # pragma: no cover
    AnnoyIndex = None  # type: ignore

try:  # pragma: no cover
    from sklearn.neighbors import NearestNeighbors
except Exception:  # pragma: no cover
    NearestNeighbors = None  # type: ignore


class VectorStore:
    """Manage vector persistence and similarity search."""

    def __init__(self, dim: int, backend: str | None = None) -> None:
        self.dim = dim
        self.backend = (backend or settings.vector_backend).lower()
        self.index_path = Path(settings.embed_dir) / f"index_{self.backend}.bin"
        self.meta_path = Path(settings.embed_dir) / f"index_{self.backend}.json"
        self._ensure_paths()
        self._load_index()

    # region setup helpers
    def _ensure_paths(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.meta_path.exists():
            self.meta_path.write_text("[]", encoding="utf-8")

    def _load_index(self) -> None:
        if self.backend == "faiss" and faiss is not None:
            self.index = faiss.IndexFlatL2(self.dim)
            if self.index_path.exists():
                try:
                    self.index = faiss.read_index(str(self.index_path))
                except Exception:
                    pass
        elif self.backend == "annoy" and AnnoyIndex is not None:
            self.index = AnnoyIndex(self.dim, "angular")
            if self.index_path.exists():
                self.index.load(str(self.index_path))
        else:
            self.backend = "sklearn"
            if NearestNeighbors is None:
                raise RuntimeError("No available vector backend")
            self.index = None
            self._load_vectors()

    # endregion

    def _load_vectors(self) -> None:
        if self.meta_path.exists():
            meta = json.loads(self.meta_path.read_text(encoding="utf-8"))
            self.vectors = np.array([m["vector"] for m in meta], dtype="float32") if meta else np.empty((0, self.dim))
            self.metadata = meta
        else:
            self.vectors = np.empty((0, self.dim))
            self.metadata = []
        if self.backend == "sklearn" and len(self.vectors) > 0 and NearestNeighbors is not None:
            self.index = NearestNeighbors(n_neighbors=min(5, len(self.vectors)), metric="cosine")
            self.index.fit(self.vectors)
        elif self.backend != "sklearn":
            self.metadata = json.loads(self.meta_path.read_text(encoding="utf-8")) if self.meta_path.exists() else []

    def _save_meta(self) -> None:
        self.meta_path.write_text(json.dumps(self.metadata, ensure_ascii=False), encoding="utf-8")

    def reset(self) -> None:
        """Clear the index for reindexing."""

        self.metadata = []
        if self.backend == "faiss" and faiss is not None:
            self.index = faiss.IndexFlatL2(self.dim)
        elif self.backend == "annoy" and AnnoyIndex is not None:
            self.index = AnnoyIndex(self.dim, "angular")
        else:
            self.vectors = np.empty((0, self.dim))
            self.index = None
        self._save_meta()
        if self.index_path.exists():
            self.index_path.unlink()

    def add(self, embeddings: np.ndarray, metadata: Sequence[dict]) -> None:
        """Add embeddings with metadata."""

        embeddings = np.asarray(embeddings, dtype="float32")
        if self.backend == "faiss" and faiss is not None:
            if getattr(self.index, "ntotal", 0) > 0:
                current = faiss.read_index(str(self.index_path)) if self.index_path.exists() else self.index
                self.index = current
            self.index.add(embeddings)
            faiss.write_index(self.index, str(self.index_path))
        elif self.backend == "annoy" and AnnoyIndex is not None:
            if getattr(self, "metadata", None) is None:
                self.metadata = []
            self.index = AnnoyIndex(self.dim, "angular")
            existing_vectors = self._existing_vectors()
            for idx, vector in enumerate(np.vstack([existing_vectors, embeddings])):
                self.index.add_item(idx, vector.tolist())
            self.index.build(10)
            self.index.save(str(self.index_path))
        else:
            self.vectors = np.vstack([self.vectors, embeddings]) if hasattr(self, "vectors") else embeddings
            if NearestNeighbors is not None and len(self.vectors) > 0:
                self.index = NearestNeighbors(n_neighbors=min(5, len(self.vectors)), metric="cosine")
                self.index.fit(self.vectors)
        self.metadata = list(getattr(self, "metadata", [])) + list(metadata)
        self._save_meta()

    def _existing_vectors(self) -> np.ndarray:
        if getattr(self, "metadata", None):
            return np.array([m["vector"] for m in self.metadata], dtype="float32")
        return np.empty((0, self.dim), dtype="float32")

    def search(self, query: np.ndarray, top_k: int = 3) -> list[Tuple[float, dict]]:
        """Perform similarity search."""

        query = np.asarray(query, dtype="float32")
        if self.backend == "faiss" and faiss is not None and getattr(self.index, "ntotal", 0) > 0:
            distances, indices = self.index.search(query.reshape(1, -1), top_k)
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1 or idx >= len(self.metadata):
                    continue
                results.append((float(dist), self.metadata[idx]))
            return results
        if self.backend == "annoy" and AnnoyIndex is not None and getattr(self, "metadata", None):
            idxs = self.index.get_nns_by_vector(query.tolist(), top_k, include_distances=True)
            results = []
            for idx, dist in zip(*idxs):
                if idx < len(self.metadata):
                    results.append((float(dist), self.metadata[idx]))
            return results
        if self.backend == "sklearn" and getattr(self, "vectors", None) is not None and len(self.vectors) > 0:
            neigh = self.index
            distances, indices = neigh.kneighbors(query.reshape(1, -1), n_neighbors=min(top_k, len(self.vectors)))
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.metadata):
                    results.append((float(dist), self.metadata[idx]))
            return results
        return []
