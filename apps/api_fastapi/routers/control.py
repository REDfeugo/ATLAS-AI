"""Planner and tool execution endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.deps import get_db
from ..services import ControlService, PlannerService

router = APIRouter(prefix="/control", tags=["control"])


@router.post("/plan", response_model=schemas.PlanResponse)
def plan(payload: schemas.PlanRequest) -> schemas.PlanResponse:
    """Return a dry-run plan for a natural language request."""

    planner = PlannerService()
    return planner.generate_plan(payload.query)


@router.post("/execute", response_model=schemas.ExecuteResult)
def execute(
    payload: schemas.ExecuteRequest,
    db: Session = Depends(get_db),
) -> schemas.ExecuteResult:
    """Execute a previously generated plan and log results."""

    service = ControlService(db)
    status, outputs, audit_ids = service.execute_plan(payload.plan, payload.confirm_token)
    return schemas.ExecuteResult(status=status, outputs=outputs, audit_ids=audit_ids)
