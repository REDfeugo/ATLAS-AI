"""Streamlit console for Atlas ARES."""

from __future__ import annotations

import os
from typing import Any, Dict

import requests
import streamlit as st

API_URL = os.getenv("ARES_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Atlas ARES Console", layout="wide")
st.title("Atlas / ARES Operator Console")

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.email = None
    st.session_state.role = "user"


def _headers() -> Dict[str, str]:
    if not st.session_state.token:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}


def _handle_request(method: str, path: str, **kwargs) -> Dict[str, Any]:
    url = f"{API_URL}{path}"
    try:
        resp = requests.request(method, url, headers=_headers() | kwargs.pop("headers", {}), timeout=30, **kwargs)
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
        return {}
    if resp.status_code >= 400:
        st.error(f"Error {resp.status_code}: {resp.text}")
        return {}
    if resp.text:
        return resp.json()
    return {}


def tab_auth() -> None:
    st.subheader("Authentication")
    with st.form("signup_form"):
        st.write("Create account")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        submitted = st.form_submit_button("Sign up")
        if submitted:
            data = _handle_request("POST", "/auth/signup", json={"email": email, "password": password})
            if data:
                st.success("Signup successful")
    with st.form("login_form"):
        st.write("Log in")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
        if submitted:
            data = _handle_request("POST", "/auth/login", json={"email": email, "password": password})
            if data and "token" in data:
                st.session_state.token = data["token"]
                st.session_state.email = email
                st.success("Logged in")
    if st.session_state.token and st.button("Logout"):
        st.session_state.token = None
        st.session_state.email = None
        st.success("Logged out")


def tab_request() -> None:
    st.subheader("Request Promotion")
    if not st.session_state.token:
        st.info("Login required")
        return
    src_model = st.text_input("Source model", value="mistral")
    dst_model = st.text_input("Destination model", value="mistral-prod")
    notes = st.text_area("Notes")
    if st.button("Submit request"):
        data = _handle_request(
            "POST",
            "/request_promotion",
            json={"src_model": src_model, "dst_model": dst_model, "notes": notes},
        )
        if data:
            st.success(f"Request #{data['id']} created")


def tab_approve() -> None:
    st.subheader("Approve Promotion")
    if not st.session_state.token:
        st.info("Login required")
        return
    request_id = st.number_input("Request ID", min_value=1, step=1)
    if st.button("Approve"):
        data = _handle_request("POST", "/approve_promotion", json={"request_id": int(request_id)})
        if data:
            st.success(f"Request #{data['id']} approved")


def tab_logs() -> None:
    st.subheader("API Logs")
    if not st.session_state.token:
        st.info("Login required")
        return
    limit = st.slider("Limit", min_value=10, max_value=200, value=50, step=10)
    if st.button("Fetch logs"):
        entries = _handle_request("GET", f"/logs?limit={limit}")
        if entries:
            st.json(entries)


def tab_ai() -> None:
    st.subheader("Local AI Chat")
    if not st.session_state.token:
        st.info("Login required")
        return
    prompt = st.text_area("Prompt")
    model = st.text_input("Model", value="mistral")
    if st.button("Send"):
        data = _handle_request("POST", "/ai/chat", json={"prompt": prompt, "model": model})
        if data:
            st.write(data.get("output"))
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍", key="chat_up"):
                    _handle_request("POST", "/feedback/record", json={"route": "ai", "model": model, "success": True})
            with col2:
                if st.button("👎", key="chat_down"):
                    _handle_request("POST", "/feedback/record", json={"route": "ai", "model": model, "success": False})


def tab_rag() -> None:
    st.subheader("RAG Operations")
    if not st.session_state.token:
        st.info("Login required")
        return
    if st.button("Index documents"):
        data = _handle_request("POST", "/rag/index")
        if data:
            st.success(f"Indexed {data['chunks_indexed']} chunks via {data['backend']}")
    query = st.text_input("Query")
    if st.button("Ask"):
        data = _handle_request("POST", "/rag/ask", json={"query": query})
        if data:
            st.write(data.get("answer"))
            st.write(data.get("citations"))


def tab_voice() -> None:
    st.subheader("Voice (Stubs)")
    if not st.session_state.token:
        st.info("Login required")
        return
    if st.button("STT Placeholder"):
        st.write(_handle_request("POST", "/voice/stt"))
    if st.button("TTS Placeholder"):
        st.write(_handle_request("POST", "/voice/tts"))


auth_tab, request_tab, approve_tab, logs_tab, ai_tab, rag_tab, voice_tab = st.tabs(
    ["Auth", "Request", "Approve", "Logs", "Local AI", "RAG", "Voice"]
)

with auth_tab:
    tab_auth()
with request_tab:
    tab_request()
with approve_tab:
    tab_approve()
with logs_tab:
    tab_logs()
with ai_tab:
    tab_ai()
with rag_tab:
    tab_rag()
with voice_tab:
    tab_voice()
