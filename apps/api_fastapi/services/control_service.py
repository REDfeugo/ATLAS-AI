"""Tool execution orchestration and permissions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from ..core.config import get_settings
from ..core.permissions import PermissionTier, requires_confirmation
from ..core.platform_adapters import load_toolkit
from ..core.schemas import ExecuteResult, PlanResponse, PlanStep
from .audit_service import AuditService
from .memory_service import MemoryService


@dataclass
class ToolDefinition:
    """Metadata describing an executable tool."""

    name: str
    summary: str
    args_schema: Dict[str, str]
    risk: str
    permission: PermissionTier
    executor: Callable[[Dict[str, object]], Dict[str, object]]


class ControlService:
    """Execute planner steps while enforcing permissions and auditing."""

    def __init__(self, session) -> None:
        self.session = session
        self.settings = get_settings()
        self.audit = AuditService(session)
        self.memory = MemoryService(session)
        self.toolkit = load_toolkit()
        self.registry = self._build_registry()
        self.user_permission = PermissionTier(self.settings.default_permission_tier.lower())

    def _build_registry(self) -> Dict[str, ToolDefinition]:
        """Create the canonical tool registry."""

        return {
            "open_app": ToolDefinition(
                name="open_app",
                summary="Launch an application by executable name",
                args_schema={"name": "Executable name, e.g. notepad"},
                risk="low",
                permission=PermissionTier.FREE,
                executor=lambda args: self.toolkit.app_control.open_app(str(args.get("name", ""))),
            ),
            "close_app": ToolDefinition(
                name="close_app",
                summary="Terminate an application by process name",
                args_schema={"name": "Process name"},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.app_control.close_app(str(args.get("name", ""))),
            ),
            "focus_window": ToolDefinition(
                name="focus_window",
                summary="Focus a window containing the provided text",
                args_schema={"title": "Substring of window title"},
                risk="low",
                permission=PermissionTier.FREE,
                executor=lambda args: self.toolkit.window_focus.focus_window(str(args.get("title", ""))),
            ),
            "set_volume": ToolDefinition(
                name="set_volume",
                summary="Set system volume percentage",
                args_schema={"percent": "0-100"},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.media_volume.set_volume(int(args.get("percent", 50))),
            ),
            "mute": ToolDefinition(
                name="mute",
                summary="Toggle mute",
                args_schema={},
                risk="low",
                permission=PermissionTier.FREE,
                executor=lambda args: self.toolkit.media_volume.mute(),
            ),
            "media_next": ToolDefinition(
                name="media_next",
                summary="Next media track",
                args_schema={},
                risk="low",
                permission=PermissionTier.FREE,
                executor=lambda args: self.toolkit.media_volume.media_next(),
            ),
            "media_playpause": ToolDefinition(
                name="media_playpause",
                summary="Toggle play/pause",
                args_schema={},
                risk="low",
                permission=PermissionTier.FREE,
                executor=lambda args: self.toolkit.media_volume.media_playpause(),
            ),
            "file_create": ToolDefinition(
                name="file_create",
                summary="Create or overwrite a file",
                args_schema={"path": "Destination path", "content": "File contents"},
                risk="high",
                permission=PermissionTier.ASK,
                executor=lambda args: self.toolkit.file_ops.create_file(
                    str(args.get("path", "")), str(args.get("content", ""))
                ),
            ),
            "file_move": ToolDefinition(
                name="file_move",
                summary="Move a file",
                args_schema={"src": "Source", "dst": "Destination"},
                risk="high",
                permission=PermissionTier.ASK,
                executor=lambda args: self.toolkit.file_ops.move_file(
                    str(args.get("src", "")), str(args.get("dst", ""))
                ),
            ),
            "file_copy": ToolDefinition(
                name="file_copy",
                summary="Copy a file",
                args_schema={"src": "Source", "dst": "Destination"},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.file_ops.copy_file(
                    str(args.get("src", "")), str(args.get("dst", ""))
                ),
            ),
            "clipboard_read": ToolDefinition(
                name="clipboard_read",
                summary="Read clipboard text",
                args_schema={},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.clipboard_ops.read_clipboard(),
            ),
            "clipboard_write": ToolDefinition(
                name="clipboard_write",
                summary="Write clipboard text",
                args_schema={"text": "Text to write"},
                risk="medium",
                permission=PermissionTier.ASK,
                executor=lambda args: self.toolkit.clipboard_ops.write_clipboard(str(args.get("text", ""))),
            ),
            "system_stats": ToolDefinition(
                name="system_stats",
                summary="Report CPU/RAM/Battery information",
                args_schema={},
                risk="low",
                permission=PermissionTier.FREE,
                executor=lambda args: self.toolkit.system_info.system_stats(),
            ),
            "open_url": ToolDefinition(
                name="open_url",
                summary="Open a URL in default browser",
                args_schema={"url": "URL"},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.web_quick_actions.open_url(str(args.get("url", ""))),
            ),
            "web_click": ToolDefinition(
                name="web_click",
                summary="Automate a click via Playwright",
                args_schema={"selector": "CSS selector"},
                risk="high",
                permission=PermissionTier.ASK,
                executor=lambda args: self.toolkit.web_quick_actions.playwright_action(
                    "click", str(args.get("selector", ""))
                ),
            ),
            "web_fill": ToolDefinition(
                name="web_fill",
                summary="Fill a field via Playwright",
                args_schema={"selector": "CSS selector", "value": "Value"},
                risk="high",
                permission=PermissionTier.ASK,
                executor=lambda args: self.toolkit.web_quick_actions.playwright_action(
                    "fill", str(args.get("selector", "")), str(args.get("value", ""))
                ),
            ),
            "screenshot_desktop": ToolDefinition(
                name="screenshot_desktop",
                summary="Capture desktop screenshot",
                args_schema={},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.screenshot.screenshot_desktop(),
            ),
            "screenshot_active": ToolDefinition(
                name="screenshot_active",
                summary="Capture active window",
                args_schema={},
                risk="medium",
                permission=PermissionTier.SAFE,
                executor=lambda args: self.toolkit.screenshot.screenshot_active(),
            ),
            "create_note": ToolDefinition(
                name="create_note",
                summary="Quick capture a note",
                args_schema={"title": "Note title", "content": "Body", "tags": "Comma tags"},
                risk="low",
                permission=PermissionTier.FREE,
                executor=self._create_note,
            ),
            "create_task": ToolDefinition(
                name="create_task",
                summary="Quick capture a task",
                args_schema={"title": "Task title", "due_date": "ISO date", "tags": "Comma tags"},
                risk="low",
                permission=PermissionTier.FREE,
                executor=self._create_task,
            ),
        }

    def list_tools(self) -> List[ToolDefinition]:
        return list(self.registry.values())

    def execute_plan(
        self, plan: PlanResponse, confirm_token: str | None
    ) -> Tuple[str, List[Dict[str, object]], List[int]]:
        """Execute a structured plan and audit each step."""

        outputs: List[Dict[str, object]] = []
        audit_ids: List[int] = []
        status = "ok"
        for step in plan.steps:
            tool = self.registry.get(step.tool)
            if not tool:
                outputs.append(
                    {
                        "tool": step.tool,
                        "status": "error",
                        "details": "Unknown tool",
                    }
                )
                status = "error"
                continue
            tier = self._effective_tier(tool)
            if requires_confirmation(step.risk, tier) and not confirm_token:
                outputs.append(
                    {
                        "tool": step.tool,
                        "status": "needs-confirmation",
                        "details": "Confirmation required for this action",
                    }
                )
                status = "pending-confirmation"
                continue
            result = tool.executor(step.args)
            result_status = str(result.get("status", "ok"))
            summary = str(result.get("details", ""))
            audit_id = self.audit.record_event(
                step.tool,
                step.args,
                summary,
                step.risk,
                confirm_token,
                succeeded=result_status != "error",
            )
            audit_ids.append(audit_id)
            outputs.append({"tool": step.tool, **result})
            if result_status == "error":
                status = "error"
        return status, outputs, audit_ids

    def dry_run(self, plan: PlanResponse) -> ExecuteResult:
        """Return a dry-run response summarizing the plan."""

        preview = [
            {
                "tool": step.tool,
                "risk": step.risk,
                "args": step.args,
            }
            for step in plan.steps
        ]
        return ExecuteResult(status="preview", outputs=preview, audit_ids=[])

    # ------------------------------------------------------------------
    # Private helpers
    def _effective_tier(self, tool: ToolDefinition) -> PermissionTier:
        """Combine global and tool-specific permission tiers (stricter wins)."""

        order = [PermissionTier.FREE, PermissionTier.SAFE, PermissionTier.ASK, PermissionTier.NEVER]
        return order[max(order.index(tool.permission), order.index(self.user_permission))]

    def _create_note(self, args: Dict[str, object]) -> Dict[str, object]:
        title = str(args.get("title", "Untitled note"))
        content = str(args.get("content", ""))
        tags_raw = args.get("tags", "")
        tags = []
        if isinstance(tags_raw, list):
            tags = [str(tag) for tag in tags_raw]
        elif isinstance(tags_raw, str) and tags_raw:
            tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
        note = self.memory.create_note(title=title, content=content, tags=tags)
        return {
            "status": "ok",
            "details": f"Note {note.id} saved",
            "note_id": note.id,
        }

    def _create_task(self, args: Dict[str, object]) -> Dict[str, object]:
        title = str(args.get("title", "Untitled task"))
        description = str(args.get("description", ""))
        due_date = args.get("due_date")
        tags_raw = args.get("tags", [])
        tags = []
        if isinstance(tags_raw, list):
            tags = [str(tag) for tag in tags_raw]
        elif isinstance(tags_raw, str) and tags_raw:
            tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
        task = self.memory.create_task(
            title=title,
            description=description,
            due_date=due_date if isinstance(due_date, str) else None,
            tags=tags,
        )
        return {
            "status": "ok",
            "details": f"Task {task.id} saved",
            "task_id": task.id,
        }
