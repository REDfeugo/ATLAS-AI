"""Plugin interface definition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Plugin(Protocol):
    name: str

    def can_handle(self, task: str) -> bool:
        ...

    def handle(self, task: str, **kwargs) -> str:
        ...


@dataclass
class SimplePlugin:
    name: str

    def can_handle(self, task: str) -> bool:
        return False

    def handle(self, task: str, **kwargs) -> str:
        raise NotImplementedError
