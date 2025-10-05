"""Expose FastAPI routers."""

from . import commands, control, health, llm, memory, notes, plugins, tasks, voice

__all__ = [
    "commands",
    "control",
    "health",
    "llm",
    "memory",
    "notes",
    "plugins",
    "tasks",
    "voice",
]
