"""Reusable command reference component."""

from __future__ import annotations

import streamlit as st

COMMANDS = [
    ("app open <name>", "Launch an application"),
    ("vol set <0-100>", "Adjust system volume"),
    ("file new <path>", "Create a new file"),
    ("clip write \"text\"", "Copy text to clipboard"),
    ("web open <url>", "Open a website"),
    ("note add \"text\"", "Capture a note"),
    ("task add \"title\" --due YYYY-MM-DD", "Capture a task"),
    ("ask \"question\"", "Send a prompt to the assistant"),
]


def render() -> None:
    """Render a gold-accented table of command examples."""

    st.markdown("### Command cheat sheet")
    for syntax, summary in COMMANDS:
        st.markdown(f"- **`{syntax}`** — {summary}")
