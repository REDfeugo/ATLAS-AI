"""Reusable message bubble component for the chat UI."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def _ensure_css() -> None:
    """Inject the shared brand stylesheet once per session."""

    if st.session_state.get("_atlas_brand_css_loaded"):
        return

    css_path = Path(__file__).resolve().parents[3] / "brand" / "theme.css"
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
    st.session_state["_atlas_brand_css_loaded"] = True


def render(role: str, content: str) -> None:
    """Render a chat bubble with brand-aligned styling."""

    _ensure_css()
    role_class = "assistant" if role == "assistant" else "user"
    heading = "Atlas" if role == "assistant" else "You"

    st.markdown(
        f"""
        <div class="atlas-bubble atlas-bubble--{role_class}">
            <strong>{heading}</strong><br/>{content}
        </div>
        """,
        unsafe_allow_html=True,
    )
