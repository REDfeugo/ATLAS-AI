"""Task CRUD endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.deps import get_db
from ..services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)) -> list[schemas.TaskRead]:
    service = TaskService(db)
    tasks = service.list_tasks()
    return [schemas.TaskRead.from_orm(task) for task in tasks]


@router.post("", response_model=schemas.TaskRead)
def create_task(
    payload: schemas.TaskCreate, db: Session = Depends(get_db)
) -> schemas.TaskRead:
    service = TaskService(db)
    task = service.create_task(payload.dict())
    return schemas.TaskRead.from_orm(task)


@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)
) -> schemas.TaskRead:
    service = TaskService(db)
    task = service.update_task(task_id, payload.dict())
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return schemas.TaskRead.from_orm(task)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict:
    service = TaskService(db)
    service.delete_task(task_id)
    return {"status": "deleted"}
