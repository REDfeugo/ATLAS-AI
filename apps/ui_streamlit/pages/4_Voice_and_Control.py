"""Voice controls and planner execution UI."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from apps.ui_streamlit.components import brand_header
from apps.ui_streamlit.utils import audio_io, i18n, state

PAGE_ICON = str(Path(__file__).resolve().parents[2] / "brand" / "atlas_avatar.svg")

st.set_page_config(page_title="Voice & Control", page_icon=PAGE_ICON, layout="wide")


def main() -> None:
    """Render voice transcription and planner tooling."""

    app_state = state.get_app_state()
    health = app_state.api_client.health_check()
    lang = app_state.language

    col_header, col_settings = st.columns([3, 1])
    with col_header:
        brand_header.render(
            title=i18n.t("voice_title", lang),
            subtitle="Speak commands, inspect plans, and drive Windows skills.",
            health_payload=health,
            mode_label="Local-first",
        )
    with col_settings:
        app_state.language = st.selectbox("Language", ["en", "es"], index=["en", "es"].index(lang))

    st.markdown("### Push-to-talk")
    devices = audio_io.list_input_devices()
    device_name = st.selectbox("Input device", options=devices or ["Default"], index=0)
    duration = st.slider("Capture length (seconds)", 1.0, 8.0, 4.0)

    if st.button(i18n.t("push_to_talk", app_state.language)):
        try:
            device_index = devices.index(device_name) if device_name in devices else None
            recording = audio_io.record(seconds=duration, device=device_index)
            payload = recording.as_base64()
            response = app_state.api_client.transcribe(payload, lang=app_state.language)
            app_state.transcript_history.append(response["text"])
        except Exception as exc:
            st.error(f"Recording failed: {exc}")

    st.markdown(f"#### {i18n.t('transcript', app_state.language)}")
    if app_state.transcript_history:
        for idx, item in enumerate(reversed(app_state.transcript_history[-5:]), start=1):
            st.markdown(f"{idx}. {item}")
    else:
        st.info("No transcripts yet. Hold the push-to-talk button to record a phrase.")

    st.markdown("### Planner preview")
    query = st.text_area(
        "Describe the task",
        value="Open Notepad, type 'Hello Atlas', save to Desktop as hello.txt, then read it back",
    )
    if st.button("Generate plan"):
        plan = app_state.api_client.plan(query)
        st.session_state["planner_preview"] = plan
    plan = st.session_state.get("planner_preview")
    if plan:
        st.json(plan)
        if st.button("Execute plan", type="primary"):
            result = app_state.api_client.execute_plan(plan)
            if result.get("status") == "pending-confirmation":
                result = app_state.api_client.execute_plan(plan, confirm_token="user-confirmed")
            st.session_state["planner_result"] = result
    result = st.session_state.get("planner_result")
    if result:
        st.success(result["status"])
        st.json(result)

    st.caption("BEGINNER TIP: The planner is heuristic offline. Swap in an LLM via PlannerService.generate_plan().")


if __name__ == "__main__":
    main()
