"""Authentication tests."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_signup_and_login(client: TestClient) -> None:
    payload = {"email": "user@example.com", "password": "password123"}
    resp = client.post("/auth/signup", json=payload)
    assert resp.status_code == 200
    token_resp = client.post("/auth/login", json=payload)
    assert token_resp.status_code == 200
    assert "token" in token_resp.json()


def test_login_wrong_password(client: TestClient) -> None:
    client.post("/auth/signup", json={"email": "user2@example.com", "password": "password123"})
    resp = client.post("/auth/login", json={"email": "user2@example.com", "password": "wrong"})
    assert resp.status_code == 401
