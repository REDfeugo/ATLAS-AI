"""Rule-based planner that can be swapped for an LLM."""

from __future__ import annotations

import re
from typing import List

from ..core.config import get_settings
from ..core.schemas import PlanResponse, PlanStep

settings = get_settings()


class PlannerService:
    """Generate deterministic plans that keep tests offline-friendly."""

    def __init__(self) -> None:
        self.settings = settings

    def generate_plan(self, query: str) -> PlanResponse:
        """Return a compact plan derived from the user's query."""

        lower = query.lower()
        steps: List[PlanStep] = []
        quoted = self._extract_quote(query)
        if "open" in lower and "notepad" in lower:
            steps.append(
                PlanStep(
                    tool="open_app",
                    args={"name": "notepad"},
                    rationale="Open Notepad to provide a visible workspace.",
                    risk="low",
                )
            )
        if "type" in lower and quoted:
            steps.append(
                PlanStep(
                    tool="clipboard_write",
                    args={"text": quoted},
                    rationale="Load the requested text into the clipboard for quick paste.",
                    risk="medium",
                )
            )
        if "save" in lower:
            path = "%USERPROFILE%\\Desktop\\hello.txt" if "desktop" in lower else "data/storage/hello.txt"
            steps.append(
                PlanStep(
                    tool="file_create",
                    args={"path": path, "content": quoted or "Atlas note"},
                    rationale="Persist the content to disk.",
                    risk="high",
                )
            )
        if "read" in lower:
            steps.append(
                PlanStep(
                    tool="open_app",
                    args={"name": "notepad"},
                    rationale="Re-open the saved file for review.",
                    risk="low",
                )
            )
        if not steps:
            steps.append(
                PlanStep(
                    tool="system_stats",
                    args={},
                    rationale="Fallback status report for unrecognised instructions.",
                    risk="low",
                )
            )
        notes = (
            "Plan generated offline using heuristics. EDIT HERE to swap with an LLM call"
        )
        return PlanResponse(steps=steps[: self.settings.max_tool_steps], notes=notes)

    def _extract_quote(self, query: str) -> str | None:
        match = re.search(r"'([^']+)'|\"([^\"]+)\"", query)
        if not match:
            return None
        return match.group(1) or match.group(2)
