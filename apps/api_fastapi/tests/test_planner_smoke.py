"""Planner smoke tests."""

from ..services.planner_service import PlannerService


def test_planner_generates_steps() -> None:
    planner = PlannerService()
    plan = planner.generate_plan(
        "Open Notepad, type 'Hello Atlas', save to Desktop as hello.txt, then read it back"
    )
    assert plan.steps
    assert any(step.tool == "file_create" for step in plan.steps)
