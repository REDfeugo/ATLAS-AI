"""Tests for semantic search service."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..core import models
from ..services.memory_service import MemoryService


def setup_database() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    models.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_semantic_search_returns_results() -> None:
    session = setup_database()
    service = MemoryService(session)
    service.create_note("Test Note", "Atlas loves local-first AI", ["ai"])
    service.create_task("Test Task", "Remember to hydrate", None, ["health"])

    results = service.semantic_search("local AI", top_k=2)
    assert results
    assert any(result["type"] == "note" for result in results)
