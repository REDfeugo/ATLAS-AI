"""Memory operations for chats, notes, and embeddings."""

from __future__ import annotations

import json
from typing import Iterable, List

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core import models
from ..core.config import get_settings
from .embed_service import EmbeddingService

settings = get_settings()


class MemoryService:
    """Persist and query chats, notes, and semantic embeddings."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.embed_service = EmbeddingService()

    def save_chat_messages(self, messages: Iterable[dict]) -> None:
        """Persist chat messages in the database."""

        for msg in messages:
            role = getattr(msg, "role", None) or msg["role"]
            content = getattr(msg, "content", None) or msg["content"]
            record = models.ChatMessage(role=role, content=content)
            self.session.add(record)

    def recall_last_messages(self, limit: int = 5) -> List[models.ChatMessage]:
        """Return the most recent chat messages."""

        stmt = select(models.ChatMessage).order_by(models.ChatMessage.id.desc()).limit(limit)
        return list(reversed(self.session.scalars(stmt).all()))

    def create_note(self, title: str, content: str, tags: List[str]) -> models.Note:
        note = models.Note(title=title, content=content, tags=json.dumps(tags))
        self.session.add(note)
        self.session.flush()
        self._store_embedding("note", note.id, f"{title}\n{content}")
        return note

    def list_notes(self) -> List[models.Note]:
        stmt = select(models.Note).order_by(models.Note.id.desc())
        return list(self.session.scalars(stmt).all())

    def delete_note(self, note_id: int) -> None:
        note = self.session.get(models.Note, note_id)
        if note:
            self.session.delete(note)
            self._delete_embedding("note", note_id)

    def _parse_due_date(self, due_date: str | None):
        """Convert ISO formatted string to date."""

        if not due_date:
            return None
        try:
            from datetime import date

            return date.fromisoformat(due_date)
        except ValueError:
            return None

    def create_task(
        self, title: str, description: str, due_date: str | None, tags: List[str]
    ) -> models.Task:
        task = models.Task(
            title=title,
            description=description,
            due_date=self._parse_due_date(due_date) if isinstance(due_date, str) else due_date,
            tags=json.dumps(tags),
        )
        self.session.add(task)
        self.session.flush()
        self._store_embedding(
            "task", task.id, f"{title}\n{description}\nTags: {', '.join(tags)}"
        )
        return task

    def list_tasks(self) -> List[models.Task]:
        stmt = select(models.Task).order_by(models.Task.due_date)
        return list(self.session.scalars(stmt).all())

    def update_task(self, task_id: int, payload: dict) -> models.Task | None:
        task = self.session.get(models.Task, task_id)
        if not task:
            return None
        for key, value in payload.items():
            if key == "tags" and value is not None:
                setattr(task, key, json.dumps(value))
            elif key == "due_date" and value:
                task.due_date = self._parse_due_date(value)
            elif value is not None:
                setattr(task, key, value)
        self._store_embedding(
            "task", task.id, f"{task.title}\n{task.description}\nTags: {task.tags_list()}"
        )
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.session.get(models.Task, task_id)
        if task:
            self.session.delete(task)
            self._delete_embedding("task", task_id)

    def semantic_search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search notes and tasks by semantic similarity."""

        query_vec = self.embed_service.embed([query])[0]
        stmt = select(models.Embedding)
        matches = []
        for embedding in self.session.scalars(stmt).all():
            vector = np.frombuffer(embedding.vector, dtype=np.float32)
            score = self.embed_service.cosine_similarity(query_vec, vector)
            matches.append((embedding, score))
        matches.sort(key=lambda item: item[1], reverse=True)
        results = []
        for embedding, score in matches[:top_k]:
            if embedding.item_type == "note":
                note = self.session.get(models.Note, embedding.item_id)
                if note:
                    results.append(
                        {
                            "type": "note",
                            "id": note.id,
                            "score": score,
                            "title": note.title,
                            "extract": note.content[:200],
                        }
                    )
            elif embedding.item_type == "task":
                task = self.session.get(models.Task, embedding.item_id)
                if task:
                    results.append(
                        {
                            "type": "task",
                            "id": task.id,
                            "score": score,
                            "title": task.title,
                            "extract": task.description[:200],
                        }
                    )
        return results

    def _store_embedding(self, item_type: str, item_id: int, text: str) -> None:
        vector = self.embed_service.embed([text])[0]
        record = self.session.query(models.Embedding).filter_by(
            item_type=item_type, item_id=item_id
        ).one_or_none()
        if record:
            record.vector = vector.tobytes()
        else:
            record = models.Embedding(item_type=item_type, item_id=item_id, vector=vector.tobytes())
            self.session.add(record)

    def _delete_embedding(self, item_type: str, item_id: int) -> None:
        record = self.session.query(models.Embedding).filter_by(
            item_type=item_type, item_id=item_id
        ).one_or_none()
        if record:
            self.session.delete(record)
