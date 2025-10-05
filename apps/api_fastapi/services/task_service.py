"""Task-specific service functions."""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from ..core import models
from .memory_service import MemoryService


class TaskService:
    """High level operations for tasks."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.memory = MemoryService(session)

    def list_tasks(self) -> List[models.Task]:
        return self.memory.list_tasks()

    def create_task(self, payload: dict) -> models.Task:
        return self.memory.create_task(
            payload["title"],
            payload.get("description", ""),
            payload.get("due_date"),
            payload.get("tags", []),
        )

    def update_task(self, task_id: int, payload: dict) -> models.Task | None:
        return self.memory.update_task(task_id, payload)

    def delete_task(self, task_id: int) -> None:
        self.memory.delete_task(task_id)
