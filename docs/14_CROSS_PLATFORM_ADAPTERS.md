# Cross-Platform Adapters

While v0.7 targets Windows, the architecture anticipates macOS/Linux:

* `apps/api_fastapi/core/platform_adapters.py` selects the skill package based on
  `platform.system()`.
* `skills/posix/` contains stubs that raise `NotImplementedError` until ported.

## Porting checklist

1. Implement equivalents for each tool in `skills/windows/` using native automation APIs
   (e.g., `osascript` on macOS, `xdotool` on Linux).
2. Respect the same return structure `{"status", "details"}` for compatibility.
3. Update `ControlService._build_registry` only if argument names differ.
4. Document OS-specific prerequisites in this file and `docs/06_WINDOWS_CONTROL_SKILLS.md`.
5. Add automated tests that simulate the POSIX implementations.

## Known blockers

* Playwright automation requires browser installation; ensure headless mode is supported.
* Clipboard manipulation differs across platforms; consider `pyperclip` alternatives.

## Contribution notes

Keep POSIX-specific dependencies optional to avoid bloating Windows installations. Add
extras to `pyproject.toml` when features land.
