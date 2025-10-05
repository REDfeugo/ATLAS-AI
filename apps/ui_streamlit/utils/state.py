"""Helper functions to manage Streamlit session state."""

from __future__ import annotations

from dataclasses import dataclass, field

import streamlit as st

from .api_client import AtlasAPIClient


@dataclass
class AppState:
    """Container for shared UI utilities."""

    api_client: AtlasAPIClient
    transcript_history: list[str] = field(default_factory=list)
    language: str = "en"


def _init_state() -> None:
    """Ensure session state has an `AppState` instance."""

    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState(api_client=AtlasAPIClient())


def get_app_state() -> AppState:
    """Return the lazily initialised application state."""

    _init_state()
    return st.session_state.app_state


def reset() -> None:
    """Clear all state for debugging purposes."""

    st.session_state.clear()
