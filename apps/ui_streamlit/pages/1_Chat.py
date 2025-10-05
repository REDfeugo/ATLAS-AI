"""Primary chat interface."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from apps.ui_streamlit.components import brand_header
from apps.ui_streamlit.utils import api_client, state

PAGE_ICON = str(Path(__file__).resolve().parents[2] / "brand" / "atlas_avatar.svg")

st.set_page_config(page_title="Chat", page_icon=PAGE_ICON)


def main() -> None:
    """Display the chat layout with history and slash-command support."""

    app_state = state.get_app_state()
    health = app_state.api_client.health_check()

    brand_header.render(
        title="Atlas Chat",
        subtitle="Converse privately with your local model or trigger commands with / syntax.",
        health_payload=health,
        mode_label="Local-first" if not health["checks"]["openai"]["configured"] else "Auto",
    )

    history = st.session_state.setdefault("chat_history", [])
    mode = st.radio("Model routing", ["auto", "local", "cloud"], horizontal=True)

    chat_container = st.container()
    with chat_container:
        for message in history:
            api_client.render_message(message)

    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_area("Your message", key="chat_input", height=120)
        submitted = st.form_submit_button("Send")

    if submitted and user_message.strip():
        content = user_message.strip()
        if content.startswith("/"):
            command = content[1:]
            with st.spinner("Parsing command..."):
                parsed = app_state.api_client.parse_command(command)
            st.session_state["chat_command_parse"] = parsed
            if parsed.get("plan"):
                plan = parsed["plan"]
                result = app_state.api_client.execute_plan(plan)
                if result.get("status") == "pending-confirmation":
                    result = app_state.api_client.execute_plan(plan, confirm_token="user-confirmed")
                history.append({"role": "user", "content": content})
                history.append({"role": "assistant", "content": f"Command executed: {result}"})
                st.session_state.chat_history = history
                st.experimental_rerun()
            elif parsed.get("action"):
                action = parsed["action"]
                if action["tool"] == "ask":
                    question = action["args"].get("question", "")
                    history.append({"role": "user", "content": question})
                    with st.spinner("Atlas is thinking..."):
                        reply = app_state.api_client.chat(question, history, mode)
                    history.append({"role": "assistant", "content": reply["reply"]})
                    st.session_state.chat_history = history
                    st.experimental_rerun()
                else:
                    history.append({"role": "user", "content": content})
                    history.append(
                        {
                            "role": "assistant",
                            "content": "Command routed to dedicated page. See Command Line tab.",
                        }
                    )
                    st.session_state.chat_history = history
                    st.experimental_rerun()
        else:
            history.append({"role": "user", "content": content})
            with st.spinner("Atlas is thinking..."):
                reply = app_state.api_client.chat(content, history, mode)
            history.append({"role": "assistant", "content": reply["reply"]})
            st.session_state.chat_history = history
            st.experimental_rerun()

    parsed = st.session_state.get("chat_command_parse")
    if parsed:
        st.markdown("### Last command preview")
        st.json(parsed)

    st.caption(
        "BEGINNER TIP: Use `/task`, `/note`, `/web` prefixes to trigger planner-backed commands."
    )


if __name__ == "__main__":
    main()
