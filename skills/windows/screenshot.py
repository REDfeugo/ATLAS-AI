"""Screenshot helpers."""

from __future__ import annotations

import platform
from pathlib import Path
from typing import Dict

try:
    import pyautogui  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyautogui = None

IS_WINDOWS = platform.system() == "Windows"
OUTPUT_DIR = Path("data/storage/screens")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def screenshot_desktop() -> Dict[str, str]:
    if not pyautogui:
        return {"status": "error", "details": "pyautogui unavailable"}
    path = OUTPUT_DIR / "desktop.png"
    pyautogui.screenshot(str(path))
    return {"status": "ok" if IS_WINDOWS else "simulated", "details": f"Saved {path}"}


def screenshot_active() -> Dict[str, str]:
    # WHY: pyautogui lacks direct active-window capture; reuse full screenshot.
    return screenshot_desktop()
