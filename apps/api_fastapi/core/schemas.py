"""Pydantic schemas shared across routers."""

from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    """Serialized chat message."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """Incoming chat request from the UI."""

    message: str
    history: List[ChatMessageSchema] = Field(default_factory=list)
    mode: str | None = Field(default=None, description="local | cloud | auto")


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
    source_path: Optional[str] = None


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
    permission: str | None = None


class HealthResponse(BaseModel):
    status: str
    versions: Dict[str, str]
    message: Optional[str] = None
    checks: Dict[str, Dict[str, str]] | None = None


class PlanStep(BaseModel):
    """Single step produced by the planner."""

    tool: str
    args: Dict[str, object]
    rationale: str
    risk: str = "low"


class PlanResponse(BaseModel):
    """Full plan returned by the planner."""

    steps: List[PlanStep]
    notes: str = ""


class PlanRequest(BaseModel):
    query: str


class ExecuteRequest(BaseModel):
    plan: PlanResponse
    confirm_token: Optional[str] = None


class ExecuteResult(BaseModel):
    status: str
    outputs: List[Dict[str, object]]
    audit_ids: List[int]


class CommandParseRequest(BaseModel):
    text: str


class CommandAction(BaseModel):
    """Result of a direct command execution without planner involvement."""

    tool: str
    args: Dict[str, object]


class CommandParseResponse(BaseModel):
    """Structured interpretation of CLI-style commands."""

    mode: str
    preview: str
    plan: Optional[PlanResponse] = None
    action: Optional[CommandAction] = None


class VoiceTranscriptionRequest(BaseModel):
    audio_base64: str
    lang: str = "en"


class VoiceTranscriptionResponse(BaseModel):
    text: str
    lang: str
    confidence: float
