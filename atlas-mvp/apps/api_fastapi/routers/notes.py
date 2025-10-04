"""Note CRUD endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.deps import get_db
from ..services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[schemas.NoteRead])
def list_notes(db: Session = Depends(get_db)) -> list[schemas.NoteRead]:
    service = NoteService(db)
    notes = service.list_notes()
    return [schemas.NoteRead.from_orm(note) for note in notes]


@router.post("", response_model=schemas.NoteRead)
def create_note(
    payload: schemas.NoteCreate, db: Session = Depends(get_db)
) -> schemas.NoteRead:
    service = NoteService(db)
    note = service.create_note(payload.dict())
    return schemas.NoteRead.from_orm(note)


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)) -> dict:
    service = NoteService(db)
    service.delete_note(note_id)
    return {"status": "deleted"}
