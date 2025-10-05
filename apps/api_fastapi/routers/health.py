"""Health check endpoint."""

from __future__ import annotations

import platform

from fastapi import APIRouter

from ..core.config import get_health_metadata, get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health")
def health() -> dict:
    """Return API status and version info."""

    metadata = get_health_metadata()
    checks = {
        "ollama": {
            "configured": bool(settings.ollama_host),
        },
        "openai": {
            "configured": bool(settings.openai_api_key),
        },
    }
    return {
        "status": "ok",
        "versions": {
            "python": platform.python_version(),
            "api": "0.7",
            **metadata,
        },
        "checks": checks,
    }
