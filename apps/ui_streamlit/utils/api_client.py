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

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def health_check(self) -> Dict:
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

    def chat(self, message: str, history: List[Dict], mode: str | None = None) -> Dict:
        payload = {"message": message, "history": history[-5:]}
        if mode:
            payload["mode"] = mode
        response = requests.post(self._url("/llm/chat"), json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

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

    def plan(self, query: str) -> Dict:
        response = requests.post(self._url("/control/plan"), json={"query": query}, timeout=20)
        response.raise_for_status()
        return response.json()

    def execute_plan(self, plan: Dict, confirm_token: str | None = None) -> Dict:
        payload = {"plan": plan, "confirm_token": confirm_token}
        response = requests.post(self._url("/control/execute"), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def parse_command(self, text: str) -> Dict:
        response = requests.post(self._url("/commands/parse"), json={"text": text}, timeout=10)
        response.raise_for_status()
        return response.json()

    def transcribe(self, audio_base64: str, lang: str) -> Dict:
        response = requests.post(
            self._url("/voice/transcribe"),
            json={"audio_base64": audio_base64, "lang": lang},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def render_message(message: Dict) -> None:
    """Render a chat message using the reusable component."""

    message_bubble.render(message["role"], message["content"])
