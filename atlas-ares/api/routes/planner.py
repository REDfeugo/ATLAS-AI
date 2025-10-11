"""Planner endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from .. import schemas
from ..config import settings
from ..logging_utils import append_log
from ..security import get_current_user
from ..services.planner_core import Planner, Tool

router = APIRouter()


def _analyze(goal: str) -> str:
    if settings.confirm_before_write and "write" in goal.lower():
        return "Guarded: confirmation required before writing."
    return f"Analysis: key objectives for {goal[:80]} identified."


def _summarize(goal: str) -> str:
    return f"Complete: deliverable summary prepared for {goal[:80]}"


@router.post("/execute", response_model=schemas.PlannerResponse)
def execute_plan(payload: schemas.PlannerRequest, user=Depends(get_current_user)) -> schemas.PlannerResponse:
    """Run the simple planner loop."""

    tools = [
        Tool(name="analyze", description="Review goal and extract tasks", handler=_analyze),
        Tool(name="summarize", description="Summarize outcome", handler=_summarize),
    ]
    planner = Planner(goal=payload.goal, tools=tools, dry_run=payload.dry_run, max_steps=payload.max_steps or settings.max_plan_steps)
    steps, final_result, halted = planner.run()
    step_models = [schemas.PlannerStep(step=i + 1, action=action, result=result) for i, (action, result) in enumerate(steps)]
    append_log("plan_finished", user=user.email, path="/plan/execute", status="ok")
    return schemas.PlannerResponse(steps=step_models, final_result=final_result, halted=halted)
