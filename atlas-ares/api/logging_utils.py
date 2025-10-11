"""Utilities for structured JSONL logging."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .config import settings


LOG_PATH = Path(settings.log_file)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_PATH.touch(exist_ok=True)


def redact(value: Optional[str]) -> Optional[str]:
    """Redact sensitive strings (very simple heuristic)."""

    if not value:
        return value
    if "@" in value or len(value) > 32:
        return "***"
    return value


def append_log(event: str, user: Optional[str] = None, path: Optional[str] = None, **extra: Any) -> None:
    """Append a JSON line to the log file."""

    entry: Dict[str, Any] = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": event,
    }
    if user:
        entry["user"] = redact(user)
    if path:
        entry["path"] = path
    entry.update({k: v for k, v in extra.items() if v is not None})
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
