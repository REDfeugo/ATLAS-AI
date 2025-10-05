"""Remove the SQLite database for a clean slate."""

from __future__ import annotations

from apps.api_fastapi.core.config import get_settings


def reset() -> None:
    """Delete the SQLite database file if it exists."""

    settings = get_settings()
    db_path = settings.db_path
    if db_path.exists():
        db_path.unlink()
        print(f"Deleted {db_path}")
    else:
        print("No database file found; nothing to remove.")


if __name__ == "__main__":
    reset()
