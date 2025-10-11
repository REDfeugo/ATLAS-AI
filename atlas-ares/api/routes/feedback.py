"""Feedback endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..logging_utils import append_log
from ..models import Feedback, User
from ..security import get_current_user
from ..services.bandit import EpsilonGreedyBandit

router = APIRouter()


@router.post("/record", response_model=schemas.Message)
def record_feedback(
    payload: schemas.FeedbackRecord,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> schemas.Message:
    """Record feedback and update bandit policy."""

    feedback = Feedback(
        user_id=user.id,
        task_id=payload.task_id,
        route=payload.route,
        model=payload.model,
        plugin=payload.plugin,
        success=payload.success,
    )
    db.add(feedback)
    db.commit()
    if payload.model:
        bandit = EpsilonGreedyBandit(db)
        bandit.record(f"model::{payload.model}", payload.success)
    append_log("feedback", user=user.email, path="/feedback/record", status="ok")
    return schemas.Message(message="feedback recorded")
