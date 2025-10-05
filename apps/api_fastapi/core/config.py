"""Application configuration helpers."""

from __future__ import annotations

import functools
import os
import platform
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# WHY: Loading environment variables early allows both API and UI to share settings.
load_dotenv()


class Settings:
    """Central configuration object for the API."""

    def __init__(self) -> None:
        # EDIT HERE: Update defaults if you want a different local model.
        self.model_name = os.getenv("MODEL_NAME", "llama3.2:3b")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.db_path = Path(os.getenv("DB_PATH", "./data/atlas.db"))
        self.embed_model_name = os.getenv("EMBED_MODEL_NAME", "all-MiniLM-L6-v2")
        self.voice_wakeword = os.getenv("VOICE_WAKEWORD", "atlas")
        self.voice_vad = os.getenv("VOICE_VAD", "True").lower() == "true"
        self.voice_lang = os.getenv("VOICE_LANG", "en")
        self.tts_style = os.getenv("TTS_STYLE", "professional_butler")
        self.max_tool_steps = int(os.getenv("MAX_TOOL_STEPS", "8"))
        self.default_permission_tier = os.getenv("DEFAULT_PERMISSION_TIER", "free")
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "45"))
        self.brand_primary = os.getenv("BRAND_PRIMARY", "#E5B80B")
        self.brand_background = os.getenv("BRAND_BG", "#0B0B0E")
        self.index_documents = os.getenv("INDEX_DOCUMENTS", "false").lower() == "true"
        self.documents_path = Path(
            os.getenv("DOCUMENTS_PATH", os.path.expanduser("~/Documents"))
        )
        self.plugins_dir = Path(os.getenv("PLUGINS_DIR", "./plugins"))
        self.platform = platform.system().lower()

    def database_url(self) -> str:
        """Return a SQLite URL."""

        # WHY: `resolve()` ensures consistent path when running from different cwd.
        db_full_path = self.db_path.resolve()
        db_full_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_full_path}" if db_full_path.suffix else f"sqlite:///{db_full_path}.db"


@functools.lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance to avoid repeated disk reads."""

    return Settings()


def get_health_metadata() -> Dict[str, Any]:
    """Compute health metadata for the `/health` endpoint."""

    settings = get_settings()
    return {
        "model": settings.model_name,
        "platform": settings.platform,
        "documents_indexed": settings.index_documents,
    }
