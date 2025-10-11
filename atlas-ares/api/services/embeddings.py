"""Lazy embedding loader using sentence-transformers."""

from __future__ import annotations

from typing import Iterable

import numpy as np
from sentence_transformers import SentenceTransformer

from ..config import settings

_model: SentenceTransformer | None = None


def _load_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.default_embed_model)
    return _model


def embed_texts(texts: Iterable[str]) -> np.ndarray:
    """Embed the provided texts as numpy array."""

    model = _load_model()
    return np.array(model.encode(list(texts), convert_to_numpy=True, show_progress_bar=False))


def embed_text(text: str) -> np.ndarray:
    """Convenience helper for single text."""

    return embed_texts([text])[0]
