"""Logging utilities with PII-safe defaults."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def configure_logging() -> None:
    """Configure root logger with rotation."""

    handler = RotatingFileHandler(LOG_DIR / "atlas.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[handler])

