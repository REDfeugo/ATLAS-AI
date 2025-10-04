"""Application configuration helpers."""

from __future__ import annotations

import functools
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# WHY: Loading environment variables early allows both API and UI to share settings.
load_dotenv()


class Settings:
    """Central configuration object for the API."""

    def __init__(self) -> None:
        self.model_name = os.getenv("MODEL_NAME", "llama3:instruct")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.db_path = Path(os.getenv("DB_PATH", "./data/storage/atlas.db"))
        self.embed_model_name = os.getenv(
            "EMBED_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
        self.plugins_dir = Path(os.getenv("PLUGINS_DIR", "./plugins"))

    def database_url(self) -> str:
        """Return a SQLite URL."""

        # WHY: `resolve()` ensures consistent path when running from different cwd.
        db_full_path = self.db_path.resolve()
        db_full_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_full_path}"


@functools.lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance to avoid repeated disk reads."""

    return Settings()


def get_health_metadata() -> Dict[str, Any]:
    """Compute health metadata for the `/health` endpoint."""

    settings = get_settings()
    return {
        "model": settings.model_name,
    }
