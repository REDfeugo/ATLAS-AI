"""Parse CLI-style commands into planner actions."""

from __future__ import annotations

import shlex
from typing import Dict, List

from ..core.schemas import (
    CommandAction,
    CommandParseRequest,
    CommandParseResponse,
    PlanResponse,
    PlanStep,
)
from .planner_service import PlannerService

class CommandService:
    """Translate textual commands into structured plans."""

    def __init__(self) -> None:
        self.planner = PlannerService()

    def parse(self, request: CommandParseRequest) -> CommandParseResponse:
        """Return a structured representation of a CLI command."""

        text = request.text.strip()
        if not text:
            return CommandParseResponse(mode="empty", preview="No command provided")
        tokens = shlex.split(text)
        head = tokens[0].lower()
        if head == "app":
            return self._parse_app(tokens)
        if head == "vol":
            return self._parse_volume(tokens)
        if head == "media":
            return self._parse_media(tokens)
        if head == "file":
            return self._parse_file(tokens)
        if head == "clip":
            return self._parse_clip(tokens)
        if head == "web":
            return self._parse_web(tokens)
        if head == "note":
            return self._parse_note(tokens)
        if head == "task":
            return self._parse_task(tokens)
        if head == "ask":
            return CommandParseResponse(
                mode="chat",
                preview="Send question to assistant",
                action=CommandAction(tool="ask", args={"question": " ".join(tokens[1:])}),
            )
        if head == "plan":
            goal = text.partition(" ")[2]
            plan = self.planner.generate_plan(goal)
            return CommandParseResponse(mode="plan", preview=f"Planner plan for: {goal}", plan=plan)
        if head == "abort":
            return CommandParseResponse(
                mode="control", preview="Signal abort", action=CommandAction(tool="abort", args={})
            )
        if head == "status":
            return CommandParseResponse(
                mode="control",
                preview="Request system status",
                action=CommandAction(tool="system_stats", args={}),
            )
        plan = self.planner.generate_plan(text)
        return CommandParseResponse(mode="plan", preview="Planner interpretation", plan=plan)

    def _single_step(self, tool: str, args: Dict[str, object], rationale: str, risk: str = "low") -> CommandParseResponse:
        step = PlanStep(tool=tool, args=args, rationale=rationale, risk=risk)
        return CommandParseResponse(mode="plan", preview=rationale, plan=PlanResponse(steps=[step]))

    def _parse_app(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 3:
            return CommandParseResponse(mode="error", preview="Usage: app <action> <name>")
        action, name = tokens[1].lower(), tokens[2]
        if action == "open":
            return self._single_step("open_app", {"name": name}, f"Open {name}")
        if action == "close":
            return self._single_step("close_app", {"name": name}, f"Close {name}", risk="medium")
        if action == "focus":
            return self._single_step("focus_window", {"title": name}, f"Focus {name}")
        return CommandParseResponse(mode="error", preview="Unknown app command")

    def _parse_volume(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 2:
            return CommandParseResponse(mode="error", preview="Usage: vol <set|mute> ...")
        action = tokens[1].lower()
        if action == "set" and len(tokens) >= 3:
            return self._single_step(
                "set_volume", {"percent": int(tokens[2])}, f"Set volume to {tokens[2]}%", risk="medium"
            )
        if action == "mute":
            return self._single_step("mute", {}, "Toggle mute")
        return CommandParseResponse(mode="error", preview="Unknown volume command")

    def _parse_media(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 2:
            return CommandParseResponse(mode="error", preview="Usage: media <play|pause|next>")
        action = tokens[1].lower()
        if action in {"play", "pause", "playpause"}:
            return self._single_step("media_playpause", {}, "Toggle play/pause")
        if action == "next":
            return self._single_step("media_next", {}, "Next track")
        return CommandParseResponse(mode="error", preview="Unknown media command")

    def _parse_file(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 3:
            return CommandParseResponse(mode="error", preview="Usage: file <new|move|copy> ...")
        action = tokens[1].lower()
        if action == "new":
            path = tokens[2]
            content = ""
            if "--content" in tokens:
                idx = tokens.index("--content")
                content = tokens[idx + 1] if idx + 1 < len(tokens) else ""
            return self._single_step(
                "file_create",
                {"path": path, "content": content},
                f"Create file {path}",
                risk="high",
            )
        if action == "move" and len(tokens) >= 4:
            return self._single_step(
                "file_move",
                {"src": tokens[2], "dst": tokens[3]},
                f"Move {tokens[2]} -> {tokens[3]}",
                risk="high",
            )
        if action == "copy" and len(tokens) >= 4:
            return self._single_step(
                "file_copy",
                {"src": tokens[2], "dst": tokens[3]},
                f"Copy {tokens[2]} -> {tokens[3]}",
                risk="medium",
            )
        return CommandParseResponse(mode="error", preview="Unknown file command")

    def _parse_clip(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 2:
            return CommandParseResponse(mode="error", preview="Usage: clip <read|write>")
        action = tokens[1].lower()
        if action == "read":
            return self._single_step("clipboard_read", {}, "Read clipboard", risk="medium")
        if action == "write":
            text = ""
            if len(tokens) >= 3:
                text = " ".join(tokens[2:])
            return self._single_step("clipboard_write", {"text": text}, "Write clipboard", risk="medium")
        return CommandParseResponse(mode="error", preview="Unknown clipboard command")

    def _parse_web(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 2:
            return CommandParseResponse(mode="error", preview="Usage: web <open|click|fill|screenshot> ...")
        action = tokens[1].lower()
        if action == "open" and len(tokens) >= 3:
            return self._single_step("open_url", {"url": tokens[2]}, f"Open {tokens[2]}", risk="medium")
        if action == "click" and len(tokens) >= 3:
            return self._single_step(
                "web_click", {"selector": tokens[2]}, f"Click {tokens[2]}", risk="high"
            )
        if action == "fill" and len(tokens) >= 4:
            return self._single_step(
                "web_fill",
                {"selector": tokens[2], "value": tokens[3]},
                f"Fill {tokens[2]}",
                risk="high",
            )
        if action == "screenshot":
            return self._single_step(
                "screenshot_desktop", {}, "Capture browser screenshot", risk="medium"
            )
        return CommandParseResponse(mode="error", preview="Unknown web command")

    def _parse_note(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 3:
            return CommandParseResponse(mode="error", preview="Usage: note add \"text\"")
        content = " ".join(tokens[2:])
        step = PlanStep(
            tool="create_note",
            args={"title": content[:40], "content": content, "tags": ""},
            rationale="Capture note",
            risk="low",
        )
        return CommandParseResponse(mode="plan", preview="Create note", plan=PlanResponse(steps=[step]))

    def _parse_task(self, tokens: List[str]) -> CommandParseResponse:
        if len(tokens) < 3:
            return CommandParseResponse(mode="error", preview="Usage: task add \"title\" ...")
        title = tokens[2]
        due = None
        tags: List[str] = []
        if "--due" in tokens:
            idx = tokens.index("--due")
            if idx + 1 < len(tokens):
                due = tokens[idx + 1]
        if "--tags" in tokens:
            idx = tokens.index("--tags")
            if idx + 1 < len(tokens):
                tags = [tag.strip() for tag in tokens[idx + 1].split(",") if tag]
        step = PlanStep(
            tool="create_task",
            args={"title": title, "due_date": due or "", "tags": tags},
            rationale="Capture task",
            risk="low",
        )
        return CommandParseResponse(mode="plan", preview="Create task", plan=PlanResponse(steps=[step]))
