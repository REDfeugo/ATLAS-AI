# Planner and Safety

The planner converts natural language into a JSON plan consumed by the control service.

## System prompt (embedded)

```
{
  "steps": [
    {"tool": "open_app", "args": {"name": "notepad"}, "rationale": "...", "risk": "low"}
  ],
  "notes": "..."
}
```

Allowed tools: `open_app`, `close_app`, `focus_window`, `set_volume`, `mute`, `media_next`,
`media_playpause`, `file_create`, `file_move`, `file_copy`, `clipboard_read`,
`clipboard_write`, `system_stats`, `open_url`, `web_click`, `web_fill`, `screenshot_active`,
`screenshot_desktop`, `create_note`, `create_task`.

## Safety controls

* `MAX_TOOL_STEPS` limits plan length (default 8).
* `requires_confirmation` enforces confirmation for `risk="high"` and `PermissionTier.ASK`.
* `audit_events` table records tool name, args, result summary, confirmation token, success flag.
* UI exposes an **Abort** button and listens for the voice keyword “Abort”.

## Dry-run preview

`ControlService.dry_run` returns a preview with tool, risk, and args. The Streamlit UI
shows this in a gold-themed card before requesting confirmation.

## Execution summary

After execution the API returns `ExecuteResult` with outputs and audit IDs. The UI reads
the summary aloud via `TTSService` and displays a textual recap.

## Extending the planner

The default implementation (`PlannerService`) is heuristic to keep smoke tests offline.
To swap in an LLM planner:

1. Replace `PlannerService.generate_plan` with an Ollama/OpenAI call.
2. Feed the system prompt above and the user query, ensuring deterministic JSON output.
3. Update `docs/11_TESTING_AND_QA.md` with new regression steps.
