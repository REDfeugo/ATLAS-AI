"""Note service built atop memory utilities."""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from ..core import models
from .memory_service import MemoryService


class NoteService:
    """CRUD helpers for notes."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.memory = MemoryService(session)

    def list_notes(self) -> List[models.Note]:
        return self.memory.list_notes()

    def create_note(self, payload: dict) -> models.Note:
        return self.memory.create_note(
            payload["title"], payload.get("content", ""), payload.get("tags", [])
        )

    def delete_note(self, note_id: int) -> None:
        self.memory.delete_note(note_id)
