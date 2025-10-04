"""Top-of-page brand header shared across Streamlit pages."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional

import streamlit as st


def _inject_css() -> None:
    """Load the brand stylesheet once per session."""

    if st.session_state.get("_atlas_brand_css_loaded"):
        return
    css_path = Path(__file__).resolve().parents[3] / "brand" / "theme.css"
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
    st.session_state["_atlas_brand_css_loaded"] = True


def _load_avatar_data() -> str:
    """Return the base64-encoded avatar for inline embedding."""

    cache_key = "_atlas_avatar_b64"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    avatar_path = Path(__file__).resolve().parents[3] / "brand" / "atlas_avatar.svg"
    encoded = base64.b64encode(avatar_path.read_text().encode("utf-8")).decode("utf-8")
    st.session_state[cache_key] = encoded
    return encoded


def render(
    *,
    title: str = "Atlas Personal AI",
    subtitle: Optional[str] = None,
    health_payload: Optional[dict] = None,
    mode_label: str = "Local",
) -> None:
    """Render the decorative header with status chips.

    Args:
        title: Main heading text.
        subtitle: Optional supporting copy.
        health_payload: Result from `health_check` to show runtime info.
        mode_label: Quick badge indicating whether we are in Local / Cloud mode.
    """

    _inject_css()
    avatar_b64 = _load_avatar_data()

    status = (health_payload or {}).get("status", "offline").lower()
    chip_class = "atlas-chip atlas-chip--ok" if status == "ok" else "atlas-chip atlas-chip--warn"
    status_label = "Online" if status == "ok" else "Check backend"
    model_name = (health_payload or {}).get("versions", {}).get("model", "unknown")

    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""

    st.markdown(
        f"""
        <div class="atlas-header">
          <div class="atlas-header__title">
            <img src="data:image/svg+xml;base64,{avatar_b64}" alt="Atlas avatar" />
            <div>
              <h1>{title}</h1>
              {subtitle_html}
            </div>
          </div>
          <div class="atlas-header__status">
            <span class="atlas-chip">{mode_label}</span>
            <span class="{chip_class}">{status_label}</span>
            <span class="atlas-badge">Model: {model_name}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
