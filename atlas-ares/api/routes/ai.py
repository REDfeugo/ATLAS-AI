"""AI related endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..config import settings
from ..db import get_db
from ..logging_utils import append_log
from ..security import get_current_user
from ..services.bandit import select_model
from ..services.ollama_client import get_client

router = APIRouter()


@router.post("/chat", response_model=schemas.ChatResponse)
def chat(
    payload: schemas.ChatRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Perform a chat completion through Ollama."""

    candidates = {payload.model, settings.default_chat_model, "llama3"}
    options = [model for model in candidates if model]
    model_choice = select_model(db, options) if options else settings.default_chat_model
    client = get_client()
    result = client.chat(
        prompt=payload.prompt,
        model=model_choice,
        temperature=payload.temperature or 0.7,
        max_tokens=payload.max_tokens or 512,
    )
    append_log("chat", user=user.email, path="/ai/chat", status="ok", detail=model_choice)
    return schemas.ChatResponse(**result)
