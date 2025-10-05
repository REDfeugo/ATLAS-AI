"""CLI-style command interface."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from apps.ui_streamlit.components import brand_header, command_help
from apps.ui_streamlit.utils import state

PAGE_ICON = str(Path(__file__).resolve().parents[2] / "brand" / "atlas_avatar.svg")

st.set_page_config(page_title="Command Line", page_icon=PAGE_ICON)


def main() -> None:
    """Render a terminal-inspired command runner."""

    app_state = state.get_app_state()
    health = app_state.api_client.health_check()

    brand_header.render(
        title="Command Line",
        subtitle="Type commands, preview plans, and execute with confirmations.",
        health_payload=health,
        mode_label="Local-first",
    )

    st.markdown("### Command input")
    command = st.text_input(
        "Enter a command",
        placeholder="app open notepad",
        key="command_text",
    )

    if st.button("Parse command", type="primary"):
        response = app_state.api_client.parse_command(command)
        st.session_state["command_parse"] = response
        st.session_state.pop("command_result", None)

    parsed = st.session_state.get("command_parse")
    if parsed:
        st.markdown(f"**Mode:** {parsed['mode']}")
        st.write(parsed.get("preview"))
        if parsed.get("plan"):
            st.json(parsed["plan"])
            if st.button("Run plan", key="execute_command"):
                result = app_state.api_client.execute_plan(parsed["plan"])
                if result.get("status") == "pending-confirmation":
                    result = app_state.api_client.execute_plan(parsed["plan"], confirm_token="user-confirmed")
                st.session_state["command_result"] = result
        elif parsed.get("action"):
            st.json(parsed["action"])
            st.info("Direct actions are handed off to the chat or UI components.")
    result = st.session_state.get("command_result")
    if result:
        st.success(result["status"])
        st.json(result)

    st.divider()
    command_help.render()
    st.caption("BEGINNER TIP: Update docs/16_COMMAND_GRAMMAR.md when adding new verbs.")


if __name__ == "__main__":
    main()
