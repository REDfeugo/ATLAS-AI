"""Database models."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    """User model storing authentication information."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False
    )

    promotion_requests: Mapped[list["PromotionRequest"]] = relationship(
        "PromotionRequest", back_populates="requester", cascade="all, delete-orphan"
    )


class PromotionRequest(Base):
    """Workflow for promoting models or plugins."""

    __tablename__ = "promotion_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    requested_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    src_model: Mapped[str] = mapped_column(String(128), nullable=False)
    src_version: Mapped[str] = mapped_column(String(64), nullable=True)
    dst_model: Mapped[str] = mapped_column(String(128), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False
    )
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    approved_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime(timezone=True))

    requester: Mapped[User] = relationship(
        "User", back_populates="promotion_requests", foreign_keys=[requested_by]
    )
    approver: Mapped[Optional[User]] = relationship(
        "User", foreign_keys=[approved_by], lazy="joined"
    )


class Feedback(Base):
    """User feedback entries used by the bandit."""

    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    task_id: Mapped[Optional[str]] = mapped_column(String(128))
    route: Mapped[Optional[str]] = mapped_column(String(64))
    model: Mapped[Optional[str]] = mapped_column(String(128))
    plugin: Mapped[Optional[str]] = mapped_column(String(128))
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False
    )


class Policy(Base):
    """Bandit policy stats for epsilon-greedy selection."""

    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    successes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    trials: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False
    )


class Document(Base):
    """Documents tracked for RAG operations."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False
    )


class EmbeddingMeta(Base):
    """Embedding metadata stored for vector search."""

    __tablename__ = "embedding_meta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    chunk_id: Mapped[str] = mapped_column(String(128), nullable=False)
    vector_backend: Mapped[str] = mapped_column(String(64), nullable=False)
    extra: Mapped[Optional[str]] = mapped_column(Text)

    document: Mapped[Document] = relationship("Document")
