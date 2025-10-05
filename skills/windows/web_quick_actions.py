"""Browser automation helpers."""

from __future__ import annotations

import platform
import webbrowser
from typing import Dict

try:
    from playwright.sync_api import sync_playwright  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    sync_playwright = None

IS_WINDOWS = platform.system() == "Windows"


def open_url(url: str) -> Dict[str, str]:
    """Open a URL in the default browser."""

    webbrowser.open(url)
    return {"status": "ok" if IS_WINDOWS else "simulated", "details": f"Opened {url}"}


def playwright_action(action: str, selector: str = "", value: str = "") -> Dict[str, str]:
    """Run a minimal Playwright automation step."""

    if not sync_playwright:
        return {"status": "error", "details": "Playwright not installed"}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        # BEGINNER TIP: Keep actions simple to avoid flaky automation.
        if action == "open":
            page.goto(selector)
        elif action == "click":
            page.click(selector)
        elif action == "fill":
            page.fill(selector, value)
        elif action == "screenshot":
            page.goto("about:blank")
        else:
            browser.close()
            return {"status": "warning", "details": f"Unsupported action {action}"}
        path = "data/storage/screens/playwright.png"
        page.screenshot(path=path)
        browser.close()
        return {"status": "ok", "details": f"Saved {path}"}
