"""Configuration helpers for the Atlas ARES API."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    app_env: str = os.getenv("APP_ENV", "local")
    db_url: str = os.getenv("DB_URL", "sqlite:///./data/ares.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
    log_file: str = os.getenv("LOG_FILE", "./logs/api.jsonl")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    default_chat_model: str = os.getenv("DEFAULT_CHAT_MODEL", "mistral")
    default_embed_model: str = os.getenv(
        "DEFAULT_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_backend: str = os.getenv("VECTOR_BACKEND", "faiss")
    docs_dir: str = os.getenv("DOCS_DIR", "./data/docs")
    embed_dir: str = os.getenv("EMBED_DIR", "./data/embeddings")
    max_plan_steps: int = int(os.getenv("MAX_PLAN_STEPS", "6"))
    confirm_before_write: bool = os.getenv("CONFIRM_BEFORE_WRITE", "true").lower() in {
        "1",
        "true",
        "yes",
    }

    @property
    def database_kwargs(self) -> dict[str, Any]:
        if self.db_url.startswith("sqlite"):
            return {"connect_args": {"check_same_thread": False}}
        return {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()


settings = get_settings()
