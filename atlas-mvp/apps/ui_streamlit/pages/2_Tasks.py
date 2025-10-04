"""Tasks CRUD page."""

import datetime as dt
from typing import List

import streamlit as st

from apps.ui_streamlit.utils import state

st.set_page_config(page_title="Tasks", page_icon="✅")


def _task_form(existing: dict | None = None) -> dict | None:
    """Render a form for creating or updating a task."""

    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Title", value=existing.get("title") if existing else "")
        description = st.text_area(
            "Description", value=existing.get("description") if existing else ""
        )
        due_date = st.date_input(
            "Due date",
            value=dt.date.fromisoformat(existing["due_date"]) if existing else dt.date.today(),
        )
        tags = st.text_input(
            "Tags (comma separated)",
            value=",".join(existing.get("tags", [])) if existing else "",
        )
        submitted = st.form_submit_button("Save task")

    if submitted and title.strip():
        return {
            "title": title,
            "description": description,
            "due_date": due_date.isoformat(),
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        }
    if submitted:
        st.warning("Please provide a task title.")
    return None


def _render_tasks(tasks: List[dict], app_state: state.AppState) -> None:
    """Display existing tasks with edit/delete controls."""

    for task in tasks:
        with st.expander(f"{task['title']} (due {task['due_date']})", expanded=False):
            st.write(task["description"] or "No description yet.")
            st.caption(
                f"Tags: {', '.join(task.get('tags', [])) if task.get('tags') else 'None'}"
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit", key=f"edit_{task['id']}"):
                    st.session_state.editing_task = task
            with col2:
                if st.button("Delete", key=f"delete_{task['id']}"):
                    app_state.api_client.delete_task(task["id"])
                    st.experimental_rerun()


def main() -> None:
    """Entrypoint for the tasks page."""

    app_state = state.get_app_state()
    st.title("✅ Tasks")
    st.caption("Stay organised by capturing todos that sync to SQLite.")

    editing_task = st.session_state.get("editing_task")
    if editing_task:
        st.info("Editing existing task")
    payload = _task_form(existing=editing_task)
    if payload:
        if editing_task:
            app_state.api_client.update_task(editing_task["id"], payload)
            st.session_state.editing_task = None
        else:
            app_state.api_client.create_task(payload)
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("Your tasks")
    tasks = app_state.api_client.list_tasks()
    if not tasks:
        st.info("No tasks yet. Add one above!")
    else:
        _render_tasks(tasks, app_state)

    st.markdown("---")
    st.caption("BEGINNER TIP: API routes in `apps/api_fastapi/routers/tasks.py`.")


if __name__ == "__main__":
    main()
