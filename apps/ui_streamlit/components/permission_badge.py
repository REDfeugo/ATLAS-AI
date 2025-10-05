"""Helper badge for rendering plugin permission tiers."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

_TIER_COPY = {
    "safe": ("Safe", "atlas-badge"),
    "ask": ("Needs confirmation", "atlas-badge"),
    "never": ("Disabled", "atlas-badge"),
}


def render(tier: str) -> None:
    """Show the tier label inside a stylised badge."""

    if st.session_state.get("_atlas_brand_css_loaded") is None:
        css_path = Path(__file__).resolve().parents[3] / "brand" / "theme.css"
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
        st.session_state["_atlas_brand_css_loaded"] = True

    label, css_class = _TIER_COPY.get(tier, (tier.title(), "atlas-badge"))
    st.markdown(f"<span class='{css_class}'>{label}</span>", unsafe_allow_html=True)
