"""Reusable message bubble component for the chat UI."""

import streamlit as st


def render(role: str, content: str) -> None:
    """Render a chat bubble with role styling."""

    color = "#DCF8C6" if role == "assistant" else "#E3F2FD"
    align = "left" if role == "assistant" else "right"

    bubble_style = (
        f"background-color: {color}; padding: 12px; border-radius: 12px; "
        f"margin-bottom: 8px; text-align: {align};"
    )
    st.markdown(
        f"<div style='{bubble_style}'><strong>{role.title()}:</strong> {content}</div>",
        unsafe_allow_html=True,
    )
