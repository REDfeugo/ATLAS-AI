"""FastAPI application wiring."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import Base, engine
from .logging_utils import append_log
from .routes import ai, approvals, auth, feedback, logs, planner, rag, voice

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Atlas ARES API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(approvals.router, tags=["approvals"])
app.include_router(logs.router, tags=["logs"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(planner.router, prefix="/plan", tags=["planner"])
app.include_router(voice.router, prefix="/voice", tags=["voice"])


@app.on_event("startup")
async def startup_event() -> None:
    append_log("startup", path="/startup", status="ok")
    logging.getLogger("uvicorn.error").info("Atlas ARES API started in %s mode", settings.app_env)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check endpoint."""

    return {"status": "ok", "env": settings.app_env}
