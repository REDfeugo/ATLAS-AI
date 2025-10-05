"""Notes management page with semantic search."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from apps.ui_streamlit.components import brand_header
from apps.ui_streamlit.utils import state

PAGE_ICON = str(Path(__file__).resolve().parents[2] / "brand" / "atlas_avatar.svg")

st.set_page_config(page_title="Notes", page_icon=PAGE_ICON)


def main() -> None:
    """Render a notes manager with semantic search."""

    app_state = state.get_app_state()
    health = app_state.api_client.health_check()

    brand_header.render(
        title="Atlas Notes",
        subtitle="Capture ideas and find them again with embeddings.",
        health_payload=health,
        mode_label="Local-first",
    )

    with st.form("note_form", clear_on_submit=True):
        title = st.text_input("Title")
        content = st.text_area("Content", height=200)
        tags = st.text_input("Tags (comma separated)")
        submitted = st.form_submit_button("Save note")
    if submitted and title.strip():
        payload = {
            "title": title,
            "content": content,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        }
        app_state.api_client.create_note(payload)
        st.experimental_rerun()
    elif submitted:
        st.warning("Please add a title before saving.")

    st.markdown("---")
    st.subheader("Semantic search")
    query = st.text_input("Search your notes", key="note_query")
    if st.button("Search") and query.strip():
        results = app_state.api_client.search_notes(query)
        if not results:
            st.markdown(
                "<div class='atlas-empty'>No semantic matches yet. Try adding more notes.</div>",
                unsafe_allow_html=True,
            )
        for res in results:
            st.write(f"**{res['title']}** — score {res['score']:.2f}")
            st.caption(res["extract"])

    st.markdown("---")
    st.subheader("All notes")
    notes = app_state.api_client.list_notes()
    if not notes:
        st.markdown(
            "<div class='atlas-empty'>No notes saved yet. Capture one above.</div>",
            unsafe_allow_html=True,
        )
    for note in notes:
        with st.expander(note["title"], expanded=False):
            st.write(note["content"])
            st.caption(f"Tags: {', '.join(note.get('tags', [])) or 'None'}")
            if st.button("Delete", key=f"note_delete_{note['id']}"):
                app_state.api_client.delete_note(note["id"])
                st.experimental_rerun()

    st.caption("BEGINNER TIP: Semantic search uses cosine similarity in SQLite.")


if __name__ == "__main__":
    main()
