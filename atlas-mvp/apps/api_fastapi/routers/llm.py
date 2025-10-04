"""LLM-related endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.deps import get_db
from ..services.llm_service import LLMService
from ..services.memory_service import MemoryService

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/chat", response_model=schemas.ChatResponse)
def chat(
    payload: schemas.ChatRequest,
    db: Session = Depends(get_db),
) -> schemas.ChatResponse:
    """Main chat endpoint bridging UI and model."""

    service = LLMService()
    memory = MemoryService(db)
    history = [msg.dict() for msg in payload.history]
    memory.save_chat_messages(history)
    response = service.chat(payload.message, history)
    memory.save_chat_messages([
        {"role": "assistant", "content": response["reply"]}
    ])
    return schemas.ChatResponse(**response)


@router.post("/voice_to_text")
def voice_to_text() -> dict:
    """Optional voice capture endpoint."""

    service = LLMService()
    return service.voice_to_text()
