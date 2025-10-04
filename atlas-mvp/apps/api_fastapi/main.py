"""FastAPI application entrypoint."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import models
from .core.banner import print_banner
from .core.db import engine
from .core.logging import configure_logging
from .routers import health, llm, memory, notes, plugins, tasks

configure_logging()
print_banner()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Atlas API", version="0.5")

# WHY: Allow local Streamlit app to call the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(llm.router)
app.include_router(memory.router)
app.include_router(tasks.router)
app.include_router(notes.router)
app.include_router(plugins.router)


@app.get("/")
def index() -> dict:
    """Simple root endpoint referencing documentation."""

    return {"message": "Welcome to Atlas API. Visit /docs for interactive documentation."}
