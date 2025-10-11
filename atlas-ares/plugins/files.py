"""Example file management plugin."""

from __future__ import annotations

from pathlib import Path

from .base import SimplePlugin


class FilePlugin(SimplePlugin):
    """Simple plugin listing files in data directory."""

    def can_handle(self, task: str) -> bool:
        return "file" in task.lower()

    def handle(self, task: str, **kwargs) -> str:
        base = Path("data")
        files = sorted(p.name for p in base.glob("**/*") if p.is_file())
        return ", ".join(files) if files else "No files found."
