"""Endpoints backing the text command interface."""

from __future__ import annotations

from fastapi import APIRouter

from ..core import schemas
from ..services import CommandService

router = APIRouter(prefix="/commands", tags=["commands"])


@router.post("/parse", response_model=schemas.CommandParseResponse)
def parse(payload: schemas.CommandParseRequest) -> schemas.CommandParseResponse:
    """Parse CLI-style commands into structured actions."""

    service = CommandService()
    return service.parse(payload)
