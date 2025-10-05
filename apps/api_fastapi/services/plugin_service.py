"""Local plugin discovery and execution."""

from __future__ import annotations

import importlib.util
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..core import models
from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class Plugin:
    """Describe a discovered plugin."""

    name: str
    description: str
    module_path: Path
    enabled: bool
    permission: str
    callable_name: str


class PluginService:
    """Manage plugin manifests and execution."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.plugins_dir = settings.plugins_dir
        self.plugins_dir.mkdir(exist_ok=True)

    def _load_manifest(self, manifest_path: Path) -> Optional[Plugin]:
        with manifest_path.open() as fh:
            manifest = yaml.safe_load(fh)
        entrypoint = manifest.get("entrypoint", "example_tool:run")
        module_name, _, callable_name = entrypoint.partition(":")
        module_filename = module_name if module_name.endswith(".py") else f"{module_name}.py"
        module_path = manifest_path.parent / module_filename
        name = manifest.get("name", manifest_path.parent.name)
        description = manifest.get("description", "No description provided")
        permission = manifest.get("permission", "ask")
        state = (
            self.session.query(models.PluginState)
            .filter(models.PluginState.name == name)
            .one_or_none()
        )
        enabled = state.enabled if state else False
        if not state:
            state = models.PluginState(name=name, enabled=enabled)
            self.session.add(state)
            self.session.flush()
        return Plugin(
            name=name,
            description=description,
            module_path=module_path,
            enabled=enabled,
            permission=permission,
            callable_name=callable_name or "run",
        )

    def discover_plugins(self) -> List[Plugin]:
        plugins: List[Plugin] = []
        for manifest in self.plugins_dir.glob("*/manifest.yaml"):
            try:
                plugin = self._load_manifest(manifest)
                if plugin:
                    plugins.append(plugin)
            except Exception as exc:  # pragma: no cover - discovery errors are rare
                logger.exception("Failed to load plugin %s: %s", manifest, exc)
        return plugins

    def set_enabled(self, name: str, enabled: bool) -> None:
        state = (
            self.session.query(models.PluginState)
            .filter(models.PluginState.name == name)
            .one_or_none()
        )
        if not state:
            state = models.PluginState(name=name, enabled=enabled)
            self.session.add(state)
        else:
            state.enabled = enabled

    def run_plugin(self, name: str, payload: Dict) -> Dict:
        plugin = next((p for p in self.discover_plugins() if p.name == name), None)
        if not plugin:
            raise HTTPException(status_code=404, detail="Plugin not found")
        if not plugin.enabled:
            raise HTTPException(status_code=400, detail="Plugin disabled")

        spec = importlib.util.spec_from_file_location(plugin.name, plugin.module_path)
        if not spec or not spec.loader:
            raise HTTPException(status_code=500, detail="Unable to load plugin module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore

        callable_name = plugin.callable_name or "run"
        if not hasattr(module, callable_name):
            raise HTTPException(status_code=500, detail="Plugin missing callable")

        result = getattr(module, callable_name)(payload)
        return {"result": result}
