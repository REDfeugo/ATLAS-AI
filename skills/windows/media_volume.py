"""Volume and media key helpers."""

from __future__ import annotations

import platform
from typing import Dict

try:
    import pyautogui  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyautogui = None

IS_WINDOWS = platform.system() == "Windows"


def set_volume(percent: int) -> Dict[str, str]:
    """Set the system volume. Simulated on non-Windows hosts."""

    percent = max(0, min(100, percent))
    if not IS_WINDOWS or pyautogui is None:
        return {"status": "simulated", "details": f"Would set volume to {percent}%"}
    # WHY: Using keyboard shortcuts avoids deeper COM dependencies.
    pyautogui.press("volumedown", presses=50)
    pyautogui.press("volumeup", presses=int(percent / 2))
    return {"status": "ok", "details": f"Volume set to ~{percent}%"}


def mute() -> Dict[str, str]:
    if not IS_WINDOWS or pyautogui is None:
        return {"status": "simulated", "details": "Would toggle mute"}
    pyautogui.press("volumemute")
    return {"status": "ok", "details": "Toggled mute"}


def media_playpause() -> Dict[str, str]:
    if not IS_WINDOWS or pyautogui is None:
        return {"status": "simulated", "details": "Would press play/pause"}
    pyautogui.press("playpause")
    return {"status": "ok", "details": "Media play/pause sent"}


def media_next() -> Dict[str, str]:
    if not IS_WINDOWS or pyautogui is None:
        return {"status": "simulated", "details": "Would press next track"}
    pyautogui.press("nexttrack")
    return {"status": "ok", "details": "Next track sent"}
