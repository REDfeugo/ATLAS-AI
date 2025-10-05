"""Clipboard helpers."""

from __future__ import annotations

import platform
from typing import Dict

try:
    import pyperclip  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyperclip = None

IS_WINDOWS = platform.system() == "Windows"


def read_clipboard() -> Dict[str, str]:
    if not pyperclip:
        return {"status": "error", "details": "pyperclip unavailable"}
    text = pyperclip.paste()
    return {"status": "ok" if IS_WINDOWS else "simulated", "details": text or ""}


def write_clipboard(text: str) -> Dict[str, str]:
    if not pyperclip:
        return {"status": "error", "details": "pyperclip unavailable"}
    pyperclip.copy(text)
    return {"status": "ok" if IS_WINDOWS else "simulated", "details": "Clipboard updated"}
