"""Streamlit entrypoint that wires the Atlas sidebar and home dashboard."""

import os
from pathlib import Path

import streamlit as st

from apps.ui_streamlit.utils import state

# BEGINNER TIP: `st.set_page_config` should be called at the top before writing any UI elements.
st.set_page_config(page_title="Atlas Assistant", page_icon="🧭", layout="wide")


def load_sidebar() -> None:
    """Render the sidebar with health status and navigation hints."""

    # WHY: Storing frequently changed values in session state avoids redundant API calls.
    app_state = state.get_app_state()

    st.sidebar.title("Atlas Control Center")
    st.sidebar.markdown(
        """
        Use the page selector below to jump between Chat, Tasks, Notes, and Plugins.
        If the backend is unreachable, double-check that `make run` is running in a
        terminal.
        """
    )

    st.sidebar.markdown("### Backend status")
    health = app_state.api_client.health_check()
    status_color = "green" if health["status"] == "ok" else "red"
    st.sidebar.markdown(f"- **Status:** :{status_color}_circle: `{health['status']}`")
    st.sidebar.markdown(f"- **API version:** `{health['versions']['api']}`")
    st.sidebar.markdown(f"- **Model:** `{health['versions']['model']}`")
    if health.get("message"):
        st.sidebar.info(health["message"])

    st.sidebar.markdown("---")
    st.sidebar.caption("Tip: Use the keyboard shortcuts menu in the Streamlit toolbar!")


def main() -> None:
    """Render the default landing page that explains the app layout."""

    load_sidebar()

    st.title("🧭 Atlas Personal AI")
    st.subheader("Welcome, explorer!")
    st.write(
        """
        Atlas is built to work **offline-first** using [Ollama](https://ollama.com/) on
        your machine. If you prefer to use OpenAI instead, supply an
        `OPENAI_API_KEY` in your `.env` file.
        """
    )

    st.markdown(
        """
        ### What can I do here?

        1. **Chat** with the assistant using the local model.
        2. Capture **tasks** and **notes** that sync to SQLite storage.
        3. Run **plugins** to extend Atlas with your own local tools.
        """
    )

    st.success("Ready when you are! Pick a page from the sidebar to begin.")

    # BEGINNER TIP: Documenting file paths helps new contributors know where to look.
    st.caption("Source: `apps/ui_streamlit/pages/` for individual page logic.")

    # Provide quick links to documentation for orientation.
    docs_dir = Path(__file__).resolve().parents[2] / "docs"
    st.markdown("### Helpful docs")
    for doc in sorted(docs_dir.glob("*.md")):
        st.markdown(f"- [{doc.name}]({os.path.relpath(doc, Path.cwd())})")


if __name__ == "__main__":
    main()
