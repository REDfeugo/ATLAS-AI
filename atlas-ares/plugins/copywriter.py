"""Example copywriter plugin."""

from __future__ import annotations

from .base import SimplePlugin


class CopywriterPlugin(SimplePlugin):
    """Generate simple marketing copy offline."""

    def can_handle(self, task: str) -> bool:
        return "copy" in task.lower()

    def handle(self, task: str, **kwargs) -> str:
        return f"Draft copy for '{task}' focusing on clarity and brevity."
