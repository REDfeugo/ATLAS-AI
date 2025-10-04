"""Chat interface that communicates with the FastAPI backend."""

from __future__ import annotations

import streamlit as st

from apps.ui_streamlit.utils import api_client, state

st.set_page_config(page_title="Chat", page_icon="💬")


def _render_voice_controls(app_state: state.AppState) -> None:
    """Render optional voice input/output toggles."""

    st.subheader("🎙️ Voice (optional milestone)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Transcribe microphone input", help="Requires SpeechRecognition"):
            transcript = app_state.api_client.voice_to_text()
            if transcript:
                st.session_state.chat_input = transcript
            else:
                st.warning("Voice recognition unavailable. Check docs milestone v0.5.")
    with col2:
        st.toggle("Enable TTS playback", key="tts_enabled")


def main() -> None:
    """Display the chat layout with history and message box."""

    app_state = state.get_app_state()

    st.title("💬 Chat with Atlas")

    # WHY: Keep the chat history in session state so the UI stays reactive when messages update.
    history = st.session_state.setdefault("chat_history", [])

    chat_container = st.container()
    with chat_container:
        for message in history:
            api_client.render_message(message)

    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_area("Your message", key="chat_input", height=120)
        submitted = st.form_submit_button("Send")

    if submitted and user_message.strip():
        history.append({"role": "user", "content": user_message})
        with st.spinner("Atlas is thinking..."):
            reply = app_state.api_client.chat(user_message, history)
        history.append({"role": "assistant", "content": reply["reply"]})
        st.session_state.chat_history = history
        st.session_state.chat_input = ""
        st.experimental_rerun()

    st.markdown("---")
    with st.expander("Voice controls"):
        _render_voice_controls(app_state)

    st.markdown("---")
    st.caption(
        "BEGINNER TIP: The chat endpoints live in `apps/api_fastapi/routers/llm.py`."
    )


if __name__ == "__main__":
    main()
