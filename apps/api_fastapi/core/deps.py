"""Reusable FastAPI dependencies."""

from __future__ import annotations

from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from . import db


def get_db() -> Iterator[Session]:
    """Yield a database session for request lifetime."""

    with db.get_session() as session:
        yield session
