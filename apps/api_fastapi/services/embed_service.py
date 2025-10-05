"""Embedding helpers using sentence-transformers."""

from __future__ import annotations

import logging
from typing import Iterable, List

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - optional dependency
    SentenceTransformer = None  # type: ignore

from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmbeddingService:
    """Create embeddings using sentence-transformers with graceful fallback."""

    def __init__(self) -> None:
        if SentenceTransformer:
            try:
                self.model = SentenceTransformer(settings.embed_model_name)
            except Exception:
                logger.warning(
                    "Failed to load %s. Falling back to random embeddings.",
                    settings.embed_model_name,
                )
                self.model = None
        else:
            self.model = None
            logger.warning("sentence-transformers not available; embeddings will be random")

    def embed(self, texts: Iterable[str]) -> List[np.ndarray]:
        """Return embedding vectors for the provided texts."""

        texts = list(texts)
        if self.model:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return [np.array(vec, dtype=np.float32) for vec in embeddings]
        rng = np.random.default_rng(42)
        return [rng.standard_normal(384).astype(np.float32) for _ in texts]

    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""

        denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)) or 1.0
        return float(np.dot(vec_a, vec_b) / denom)
