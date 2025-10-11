"""Test fixtures for API."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import config
from api.db import Base, get_db
from api.server import app


@pytest.fixture()
def temp_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(config.settings, "db_url", f"sqlite:///{db_path}")
    monkeypatch.setattr(config.settings, "log_file", str(tmp_path / "api.jsonl"))
    monkeypatch.setattr(config.settings, "docs_dir", str(tmp_path / "docs"))
    monkeypatch.setattr(config.settings, "embed_dir", str(tmp_path / "embeddings"))
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "embeddings").mkdir(exist_ok=True)


@pytest.fixture()
def client(temp_settings: None) -> TestClient:
    return TestClient(app)
