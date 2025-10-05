"""Command parser smoke tests."""

from ..core.schemas import CommandParseRequest
from ..services.command_service import CommandService


def test_command_parser_returns_plan() -> None:
    service = CommandService()
    response = service.parse(CommandParseRequest(text="app open notepad"))
    assert response.mode == "plan"
    assert response.plan is not None
    assert response.plan.steps[0].tool == "open_app"
