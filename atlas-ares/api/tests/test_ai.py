"""AI route tests with mocked Ollama."""

from __future__ import annotations

from fastapi.testclient import TestClient


class DummyClient:
    def chat(self, **kwargs):  # type: ignore[no-untyped-def]
        return {"output": "hello", "model": kwargs.get("model", "mistral"), "prompt_tokens": 1, "completion_tokens": 1}


def _auth_headers(client: TestClient) -> dict[str, str]:
    client.post("/auth/signup", json={"email": "ai@example.com", "password": "password123"})
    resp = client.post("/auth/login", json={"email": "ai@example.com", "password": "password123"})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_chat_endpoint(client: TestClient, monkeypatch) -> None:
    from api.routes import ai as ai_module

    monkeypatch.setattr(ai_module, "get_client", lambda: DummyClient())
    headers = _auth_headers(client)
    resp = client.post("/ai/chat", json={"prompt": "hi"}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["output"] == "hello"
