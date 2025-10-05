"""SQLAlchemy models for Atlas."""

from __future__ import annotations

import json
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import LargeBinary


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ChatMessage(Base):
    """Stored chat messages for recall."""

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class Task(Base):
    """Task model with tags stored as JSON string for simplicity."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    due_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    tags: Mapped[str] = mapped_column(String(255), default="[]")
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    def tags_list(self) -> List[str]:
        return json.loads(self.tags or "[]")


class Note(Base):
    """Note model with text content and tags."""

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(String(255), default="[]")

    def tags_list(self) -> List[str]:
        return json.loads(self.tags or "[]")


class Embedding(Base):
    """Embedding vectors stored as binary blobs."""

    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_type: Mapped[str] = mapped_column(String(32), nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    vector: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)


class PluginState(Base):
    """Persist plugin enable/disable state."""

    __tablename__ = "plugin_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)


class AuditEvent(Base):
    """Track every tool execution for transparency."""

    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tool_name: Mapped[str] = mapped_column(String(64), nullable=False)
    args_json: Mapped[str] = mapped_column(Text, default="{}")
    result_summary: Mapped[str] = mapped_column(Text, default="")
    risk_level: Mapped[str] = mapped_column(String(16), default="low")
    confirmation_token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    succeeded: Mapped[bool] = mapped_column(Boolean, default=True)


class DocumentChunk(Base):
    """Indexed chunk from the optional Documents ingestion pipeline."""

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_path: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
