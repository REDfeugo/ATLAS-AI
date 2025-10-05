"""Voice transcription endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ..core import schemas
from ..core.config import get_settings
from ..services import STTService

router = APIRouter(prefix="/voice", tags=["voice"])
settings = get_settings()


@router.post("/transcribe", response_model=schemas.VoiceTranscriptionResponse)
def transcribe(payload: schemas.VoiceTranscriptionRequest) -> schemas.VoiceTranscriptionResponse:
    """Transcribe a short audio clip."""

    service = STTService()
    text, confidence = service.transcribe(payload.audio_base64, payload.lang)
    return schemas.VoiceTranscriptionResponse(text=text, lang=payload.lang, confidence=confidence)
