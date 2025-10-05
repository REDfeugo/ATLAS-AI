"""Smoke test for health endpoint."""

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert "versions" in data
    assert "checks" in data
    assert "ollama" in data["checks"]
