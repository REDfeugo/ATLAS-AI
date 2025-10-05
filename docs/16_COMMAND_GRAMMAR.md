# Command Grammar

Commands follow a familiar CLI style. Quotes wrap multi-word arguments, switches use `--`.

## Core verbs

| Command | Description | Example |
|---------|-------------|---------|
| `app open <name>` | Launch an app | `app open notepad` |
| `app close <name>` | Terminate app | `app close notepad` |
| `app focus "<title>"` | Focus window | `app focus "Untitled - Notepad"` |
| `vol set <0-100>` | Set volume | `vol set 60` |
| `vol mute` | Toggle mute | `vol mute` |
| `media play|pause|next` | Media control | `media next` |
| `file new <path> --content "..."` | Create file | `file new demo.txt --content "Hi"` |
| `file move <src> <dst>` | Move file | `file move a.txt b.txt` |
| `file copy <src> <dst>` | Copy file | `file copy a.txt b.txt` |
| `clip read` | Read clipboard | `clip read` |
| `clip write "text"` | Write clipboard | `clip write "Copied!"` |
| `web open <url>` | Open URL | `web open https://github.com/` |
| `web click "selector"` | Click element | `web click "button.submit"` |
| `web fill "selector" "value"` | Fill element | `web fill "input[name=q]" "atlas"` |
| `web screenshot` | Capture screenshot | `web screenshot` |
| `note add "text"` | Create note | `note add "Standup notes"` |
| `task add "title" --due YYYY-MM-DD --tags a,b` | Create task | `task add "Renew domain" --due 2025-10-10 --tags ops,urgent` |
| `ask "question"` | Send LLM prompt | `ask "Summarise my notes"` |
| `plan "goal"` | Generate planner plan | `plan "Audit downloads"` |
| `status` | System info | `status` |
| `abort` | Trigger abort flow | `abort` |

## Extensibility

* Extend `CommandService` to parse new verbs; keep docs in sync.
* Ensure each command maps to a registered tool (or planner).
* Update smoke tests for critical grammar paths.

## Slash commands

In chat you can prefix commands with `/`. Example: `/task add "Write release notes" --due 2024-01-15`.
