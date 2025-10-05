"""File operation helpers."""

from __future__ import annotations

import platform
import shutil
from pathlib import Path
from typing import Dict

IS_WINDOWS = platform.system() == "Windows"
BASE_DIR = Path("data/storage")
BASE_DIR.mkdir(parents=True, exist_ok=True)


def _safe_path(path: str) -> Path:
    """Ensure files are stored within the sandbox unless absolute paths are used."""

    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate
    return (BASE_DIR / candidate).resolve()


def create_file(path: str, content: str) -> Dict[str, str]:
    destination = _safe_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return {
        "status": "ok" if IS_WINDOWS else "simulated",
        "details": f"Wrote {destination}",
    }


def move_file(src: str, dst: str) -> Dict[str, str]:
    source = _safe_path(src)
    destination = _safe_path(dst)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        return {"status": "error", "details": f"Source {source} missing"}
    shutil.move(str(source), str(destination))
    return {"status": "ok", "details": f"Moved {source} -> {destination}"}


def copy_file(src: str, dst: str) -> Dict[str, str]:
    source = _safe_path(src)
    destination = _safe_path(dst)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        return {"status": "error", "details": f"Source {source} missing"}
    shutil.copy2(str(source), str(destination))
    return {"status": "ok", "details": f"Copied {source} -> {destination}"}
