"""Health check endpoint."""

from __future__ import annotations

import platform

from fastapi import APIRouter

from ..core.config import get_health_metadata

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Return API status and version info."""

    metadata = get_health_metadata()
    return {
        "status": "ok",
        "versions": {
            "python": platform.python_version(),
            "api": "0.5",
            **metadata,
        },
    }
