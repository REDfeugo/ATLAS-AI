"""Window focus helpers."""

from __future__ import annotations

import platform
from typing import Dict

try:
    import pywinauto  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pywinauto = None

IS_WINDOWS = platform.system() == "Windows"


def focus_window(title_substring: str) -> Dict[str, str]:
    """Attempt to focus the first window containing the provided substring."""

    if not IS_WINDOWS or pywinauto is None:
        return {
            "status": "simulated",
            "details": f"Would focus window containing '{title_substring}'",
        }
    app = pywinauto.Application(backend="uia")
    for window in app.windows():
        if title_substring.lower() in window.window_text().lower():
            window.set_focus()
            return {"status": "ok", "details": f"Focused {window.window_text()}"}
    return {"status": "warning", "details": "Window not found"}
