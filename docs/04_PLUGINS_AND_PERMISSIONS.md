# Plugins and Permissions

Plugins live under `plugins/` and follow a minimal contract:

```
plugins/example_tool/
  manifest.yaml
  example_tool.py
  README.md
```

`manifest.yaml` fields:

```yaml
name: example_tool
entrypoint: example_tool:run
summary: Summarise knowledge base
permission: ask  # free | safe | ask | never
```

The Python module exposes `run(payload: dict) -> dict`. The API validates the plugin
allowlist before execution and stores results in the audit log.

## Permission tiers

| Tier  | Description                                    |
|-------|------------------------------------------------|
| free  | Always allowed                                 |
| safe  | Low-risk actions (system info, media keys)     |
| ask   | Requires confirmation (file writes, clipboard) |
| never | Explicitly disabled                            |

`DEFAULT_PERMISSION_TIER` in `.env` sets the baseline. The control service compares a
step's `risk` with the tool's tier using `requires_confirmation`.

## Adding a plugin

1. Duplicate `plugins/example_tool` and adjust metadata.
2. Update README with usage notes and safety considerations.
3. Restart `make run` and enable the plugin from the Streamlit Plugins page.
4. Run actions via the chat slash command `/plugin example_tool {"prompt": "..."}`.

## Brand cues

Permission badges use `brand/theme.css` classes to show status (gold for ask, slate for
safe). Confirmation modals inherit the same palette for consistent UX.
