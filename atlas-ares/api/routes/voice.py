"""Voice endpoints stubs."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from .. import schemas
from ..security import get_current_user

router = APIRouter()


@router.post("/stt", response_model=schemas.VoiceResponse)
def speech_to_text(user=Depends(get_current_user)) -> schemas.VoiceResponse:
    """Stubbed speech-to-text endpoint.

    Integrate whisper.cpp, Vosk, or other offline speech recognizers here.
    Return detected text from audio payloads.
    """

    return schemas.VoiceResponse(text="[voice input placeholder]")


@router.post("/tts", response_model=schemas.VoiceResponse)
def text_to_speech(user=Depends(get_current_user)) -> schemas.VoiceResponse:
    """Stubbed text-to-speech endpoint.

    Integrate Coqui-TTS or similar offline TTS to generate audio responses.
    Return base64-encoded audio data when implemented.
    """

    return schemas.VoiceResponse(text="[voice output placeholder]")
