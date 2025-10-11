"""Pydantic schemas for requests and responses."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Message(BaseModel):
    message: str


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PromotionRequestCreate(BaseModel):
    src_model: str
    src_version: Optional[str] = None
    dst_model: str
    notes: Optional[str] = None


class PromotionRequestResponse(BaseModel):
    id: int
    requested_by: int
    src_model: str
    src_version: Optional[str]
    dst_model: str
    notes: Optional[str]
    status: str
    created_at: dt.datetime
    approved_by: Optional[int]
    approved_at: Optional[dt.datetime]

    class Config:
        from_attributes = True


class PromotionApprovalRequest(BaseModel):
    request_id: int


class LogEntry(BaseModel):
    ts: str
    event: str
    user: Optional[str] = None
    path: Optional[str] = None
    ms: Optional[float] = None
    status: Optional[str] = None
    detail: Optional[str] = None


class ChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=512, ge=1, le=2048)


class ChatResponse(BaseModel):
    output: str
    model: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None


class RagIndexResponse(BaseModel):
    documents_indexed: int
    chunks_indexed: int
    backend: str


class RagQueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=10)


class RagCitation(BaseModel):
    path: str
    snippet: str


class RagQueryResponse(BaseModel):
    answer: str
    citations: list[RagCitation]


class FeedbackRecord(BaseModel):
    task_id: Optional[str] = None
    route: Optional[str] = None
    model: Optional[str] = None
    plugin: Optional[str] = None
    success: bool


class PlannerRequest(BaseModel):
    goal: str
    dry_run: bool = False
    max_steps: Optional[int] = None


class PlannerStep(BaseModel):
    step: int
    action: str
    result: str


class PlannerResponse(BaseModel):
    steps: list[PlannerStep]
    final_result: str
    halted: bool


class VoiceResponse(BaseModel):
    text: str
