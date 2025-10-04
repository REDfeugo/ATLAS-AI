"""Seed the SQLite database with example tasks and notes."""

from __future__ import annotations

import json
from pathlib import Path

from datetime import date

from sqlalchemy.orm import Session

from apps.api_fastapi.core import models
from apps.api_fastapi.core.db import SessionLocal, engine

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "seeds"


def load_json(name: str) -> list[dict]:
    """Load a JSON file from the seed directory."""

    with (DATA_DIR / name).open() as fh:
        return json.load(fh)


def seed() -> None:
    """Insert seed rows when the tables are empty."""

    models.Base.metadata.create_all(bind=engine)
    session: Session = SessionLocal()
    try:
        if not session.query(models.Note).count():
            for note in load_json("example_notes.json"):
                session.add(
                    models.Note(
                        title=note["title"],
                        content=note["content"],
                        tags=json.dumps(note.get("tags", [])),
                    )
                )
        if not session.query(models.Task).count():
            for task in load_json("example_tasks.json"):
                due_date = task.get("due_date")
                due_date_obj = date.fromisoformat(due_date) if due_date else None
                session.add(
                    models.Task(
                        title=task["title"],
                        description=task.get("description", ""),
                        due_date=due_date_obj,
                        tags=json.dumps(task.get("tags", [])),
                    )
                )
        session.commit()
        print("Seed data inserted.")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
