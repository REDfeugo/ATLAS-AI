"""Helper wrapper around the FastAPI backend for Streamlit pages."""

from __future__ import annotations

import json
import os
from typing import Dict, List

import requests

from ..components import message_bubble


class AtlasAPIClient:
    """Simplified HTTP client for the Atlas FastAPI backend."""

    def __init__(self) -> None:
        self.base_url = os.getenv("ATLAS_API_URL", "http://localhost:8000")

    # WHY: Small helper ensures consistent URL joining.
    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def health_check(self) -> Dict:
        """Return health status, defaulting to an offline message when unreachable."""

        try:
            response = requests.get(self._url("/health"), timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {
                "status": "offline",
                "versions": {"api": "unknown", "model": "unknown"},
                "message": "API unreachable. Is `make run` active?",
            }

    def chat(self, message: str, history: List[Dict]) -> Dict:
        """Send a chat message to the backend and return the reply payload."""

        payload = {"message": message, "history": history[-5:]}
        response = requests.post(self._url("/llm/chat"), json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    def voice_to_text(self) -> str | None:
        """Ask the backend to capture microphone input if supported."""

        try:
            response = requests.post(self._url("/llm/voice_to_text"), timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("transcript")
        except requests.RequestException:
            return None

    def list_tasks(self) -> List[Dict]:
        response = requests.get(self._url("/tasks"), timeout=10)
        response.raise_for_status()
        return response.json()

    def create_task(self, payload: Dict) -> Dict:
        response = requests.post(self._url("/tasks"), json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def update_task(self, task_id: int, payload: Dict) -> Dict:
        response = requests.put(self._url(f"/tasks/{task_id}"), json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_task(self, task_id: int) -> None:
        requests.delete(self._url(f"/tasks/{task_id}"), timeout=10)

    def list_notes(self) -> List[Dict]:
        response = requests.get(self._url("/notes"), timeout=10)
        response.raise_for_status()
        return response.json()

    def create_note(self, payload: Dict) -> Dict:
        response = requests.post(self._url("/notes"), json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_note(self, note_id: int) -> None:
        requests.delete(self._url(f"/notes/{note_id}"), timeout=10)

    def search_notes(self, query: str) -> List[Dict]:
        response = requests.post(
            self._url("/memory/semantic_search"),
            json={"query": query, "top_k": 5},
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["results"]

    def list_plugins(self) -> List[Dict]:
        try:
            response = requests.get(self._url("/plugins"), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

    def set_plugin_enabled(self, name: str, enabled: bool) -> None:
        try:
            requests.post(
                self._url("/plugins/toggle"),
                json={"name": name, "enabled": enabled},
                timeout=10,
            )
        except requests.RequestException:
            pass

    def run_plugin(self, name: str, payload: str) -> Dict:
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON payload"}
        try:
            response = requests.post(
                self._url("/plugins/run"),
                json={"name": name, "payload": parsed},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            return {"error": f"Failed to run plugin: {exc}"}


def render_message(message: Dict) -> None:
    """Render a chat message using the reusable component."""

    message_bubble.render(message["role"], message["content"])
