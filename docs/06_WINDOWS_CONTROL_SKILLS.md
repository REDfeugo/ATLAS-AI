# Windows Control Skills

The control service exposes safe wrappers around Windows automation libraries. Each tool
has metadata (summary, args, risk, permission tier) defined in
`apps/api_fastapi/services/control_service.py`.

## Skill catalogue

| Tool               | Description                          | Risk   |
|--------------------|--------------------------------------|--------|
| `open_app`         | Launch executable (Notepad, etc.)    | low    |
| `close_app`        | Terminate processes by name          | medium |
| `focus_window`     | Bring window with matching title     | low    |
| `set_volume`       | Adjust system volume                 | medium |
| `mute`             | Toggle mute                          | low    |
| `media_playpause`  | Play/pause media                     | low    |
| `media_next`       | Next track                           | low    |
| `file_create`      | Create or overwrite files            | high   |
| `file_move`        | Move files                           | high   |
| `file_copy`        | Copy files                           | medium |
| `clipboard_read`   | Read clipboard text                  | medium |
| `clipboard_write`  | Write clipboard text                 | medium |
| `system_stats`     | Report CPU/RAM/battery               | low    |
| `open_url`         | Open default browser                 | medium |
| `web_click`        | Playwright click                     | high   |
| `web_fill`         | Playwright fill                      | high   |
| `screenshot_active`| Capture active window (simulated)    | medium |
| `screenshot_desktop`| Capture desktop (pyautogui)        | medium |
| `create_note`      | Persist note via MemoryService       | low    |
| `create_task`      | Persist task via MemoryService       | low    |

## Confirmation flow

High-risk tools trigger a confirmation prompt unless a `confirm_token` is provided.
The UI surfaces this as a gold modal with step-by-step preview.

## Rollback guidance

* File operations write into `data/storage/` by default to prevent accidents.
* Clipboard writes are reversible—`clip read` shows the previous value.
* Playwright actions run headless and target placeholder pages. Extend with caution by
  adding allowlists per domain.

## Extending skills

1. Add a new function to `skills/windows/` with docstrings and simulated fallbacks.
2. Register the tool in `ControlService._build_registry` with appropriate risk tier.
3. Update `docs/16_COMMAND_GRAMMAR.md` with the new command syntax.
4. Include manual QA steps in `docs/11_TESTING_AND_QA.md`.
