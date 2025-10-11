"""Minimal planner/executor for Atlas ARES."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple

from ..config import settings
from ..logging_utils import append_log


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[[str], str]


@dataclass
class Planner:
    goal: str
    tools: List[Tool]
    max_steps: int = settings.max_plan_steps
    dry_run: bool = False
    scratchpad: List[Tuple[str, str]] = field(default_factory=list)

    def run(self) -> Tuple[List[Tuple[str, str]], str, bool]:
        """Execute the planner loop with guardrails."""

        append_log("plan_start", path="/plan/execute", detail=self.goal)
        for step in range(1, self.max_steps + 1):
            action, result = self._take_step(step)
            self.scratchpad.append((action, result))
            append_log("plan_step", path="/plan/execute", detail=f"{step}:{action}")
            if "complete" in result.lower():
                append_log("plan_complete", path="/plan/execute", detail=result)
                return self.scratchpad, result, False
        append_log("plan_halted", path="/plan/execute", detail="max steps reached")
        return self.scratchpad, "Max steps reached", True

    def _take_step(self, step: int) -> Tuple[str, str]:
        tool = self.tools[(step - 1) % len(self.tools)] if self.tools else None
        if tool is None:
            return "noop", "No tools configured"
        if self.dry_run:
            return tool.name, f"Dry run step {step} using {tool.name}"
        try:
            result = tool.handler(self.goal)
        except Exception as exc:  # pragma: no cover - defensive
            result = f"Error: {exc}"
        return tool.name, result
