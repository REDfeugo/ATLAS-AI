"""Utilities to load skill modules based on the host platform."""

from __future__ import annotations

import importlib
from typing import Any

from .config import get_settings


def load_toolkit() -> Any:
    """Import the appropriate skills module for the active platform."""

    settings = get_settings()
    if settings.platform == "windows":
        return importlib.import_module("skills.windows")
    # WHY: Until macOS/Linux support lands we reuse the Windows stubs so that the
    # developer experience stays consistent. The functions warn when running on
    # unsupported systems.
    return importlib.import_module("skills.windows")
