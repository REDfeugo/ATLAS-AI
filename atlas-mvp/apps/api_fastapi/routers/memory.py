"""Memory endpoints for semantic search."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.deps import get_db
from ..services.memory_service import MemoryService

router = APIRouter(prefix="/memory", tags=["memory"])


@router.post("/semantic_search", response_model=schemas.SemanticSearchResponse)
def semantic_search(
    payload: schemas.SemanticSearchRequest,
    db: Session = Depends(get_db),
) -> schemas.SemanticSearchResponse:
    """Return semantic search matches for notes and tasks."""

    service = MemoryService(db)
    results = service.semantic_search(payload.query, payload.top_k)
    return schemas.SemanticSearchResponse(results=results)
