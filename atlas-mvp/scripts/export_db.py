"""Export database contents to JSON for backup or sharing."""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import Session

from apps.api_fastapi.core import models
from apps.api_fastapi.core.db import SessionLocal

OUTPUT = Path("export.json")


def export() -> None:
    """Write notes and tasks to a single JSON file."""

    session: Session = SessionLocal()
    try:
        payload = {
            "notes": [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "tags": note.tags_list(),
                }
                for note in session.query(models.Note).all()
            ],
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "due_date": task.due_date,
                    "tags": task.tags_list(),
                }
                for task in session.query(models.Task).all()
            ],
        }
        OUTPUT.write_text(json.dumps(payload, indent=2))
        print(f"Exported data to {OUTPUT.resolve()}")
    finally:
        session.close()


if __name__ == "__main__":
    export()
