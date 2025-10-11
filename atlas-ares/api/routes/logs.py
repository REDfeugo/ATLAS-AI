"""Log retrieval endpoints."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query

from ..config import settings
from ..schemas import LogEntry
from ..security import get_current_user

router = APIRouter()


@router.get("/logs", response_model=list[LogEntry])
def get_logs(limit: int = Query(default=50, ge=1, le=500), user=Depends(get_current_user)) -> list[LogEntry]:
    """Return the last N log entries from the JSONL file."""

    path = Path(settings.log_file)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Log file missing")
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    selected = lines[-limit:] if limit < len(lines) else lines
    entries = []
    for line in selected:
        try:
            entries.append(LogEntry.model_validate(json.loads(line)))
        except json.JSONDecodeError:
            continue
    return entries
