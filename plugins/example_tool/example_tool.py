"""Example plugin that summarises a local text file."""

from __future__ import annotations

from pathlib import Path


def run(payload: dict) -> dict:
    """Return the first 200 characters of the requested file."""

    path = payload.get("path", "data/seeds/knowledge.txt")
    file_path = Path(path)
    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}
    text = file_path.read_text()
    summary = text[:200] + ("..." if len(text) > 200 else "")
    return {"summary": summary, "path": str(file_path)}
