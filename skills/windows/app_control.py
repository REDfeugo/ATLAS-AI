"""High-level application control utilities for Windows."""

from __future__ import annotations

import platform
import subprocess
from typing import Dict

import psutil

IS_WINDOWS = platform.system() == "Windows"


def open_app(name: str) -> Dict[str, str]:
    """Launch an application by its executable name."""

    if not IS_WINDOWS:
        return {
            "status": "simulated",
            "details": f"Would launch {name} (non-Windows host)",
        }
    try:
        subprocess.Popen(name)  # noqa: S603,S607 - controlled input from planner
        return {"status": "ok", "details": f"Launched {name}"}
    except FileNotFoundError:
        return {"status": "error", "details": f"Executable {name} not found"}


def close_app(name: str) -> Dict[str, str]:
    """Close an application by process name."""

    closed = 0
    for proc in psutil.process_iter(["name"]):
        if proc.info.get("name", "").lower() == name.lower():
            try:
                proc.terminate()
                closed += 1
            except psutil.Error:
                continue
    if closed:
        return {"status": "ok", "details": f"Closed {closed} process(es) named {name}"}
    return {"status": "warning", "details": f"No running process named {name}"}
