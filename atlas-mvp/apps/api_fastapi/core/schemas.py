"""Pydantic schemas for request/response bodies."""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    """A chat message used in history payloads."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """Incoming chat request from the UI."""

    message: str
    history: List[ChatMessageSchema] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Response returned by the LLM service."""

    reply: str
    tokens: int
    model_used: str


class TaskBase(BaseModel):
    """Shared fields for task creation/update."""

    title: str
    description: Optional[str] = ""
    due_date: Optional[date]
    tags: List[str] = Field(default_factory=list)


class TaskCreate(TaskBase):
    """Payload for creating a task."""

    pass


class TaskUpdate(TaskBase):
    """Payload for updating a task."""

    completed: Optional[bool] = None


class TaskRead(TaskBase):
    """Response representation of a task."""

    id: int
    completed: bool

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int

    class Config:
        orm_mode = True


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SemanticSearchResult(BaseModel):
    type: str
    id: int
    score: float
    title: str
    extract: str


class SemanticSearchResponse(BaseModel):
    results: List[SemanticSearchResult]


class PluginToggleRequest(BaseModel):
    name: str
    enabled: bool


class PluginRunRequest(BaseModel):
    name: str
    payload: dict


class PluginDescriptor(BaseModel):
    name: str
    description: str
    enabled: bool


class HealthResponse(BaseModel):
    status: str
    versions: dict
    message: Optional[str] = None
