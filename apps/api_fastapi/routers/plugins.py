"""Plugin endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.deps import get_db
from ..services.plugin_service import PluginService

router = APIRouter(prefix="/plugins", tags=["plugins"])


@router.get("", response_model=list[schemas.PluginDescriptor])
def list_plugins(db: Session = Depends(get_db)) -> list[schemas.PluginDescriptor]:
    service = PluginService(db)
    plugins = service.discover_plugins()
    return [
        schemas.PluginDescriptor(
            name=p.name,
            description=p.description,
            enabled=p.enabled,
            permission=p.permission,
        )
        for p in plugins
    ]


@router.post("/toggle")
def toggle_plugin(
    payload: schemas.PluginToggleRequest, db: Session = Depends(get_db)
) -> dict:
    service = PluginService(db)
    service.set_enabled(payload.name, payload.enabled)
    return {"status": "updated"}


@router.post("/run")
def run_plugin(
    payload: schemas.PluginRunRequest, db: Session = Depends(get_db)
) -> dict:
    service = PluginService(db)
    return service.run_plugin(payload.name, payload.payload)
