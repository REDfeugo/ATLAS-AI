"""Speech-to-text helpers leveraging Vosk when available."""

from __future__ import annotations

import base64
import json
from typing import Tuple

try:
    from vosk import KaldiRecognizer, Model  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    KaldiRecognizer = None  # type: ignore
    Model = None  # type: ignore


class STTService:
    """Decode base64 audio and run offline transcription when possible."""

    def __init__(self) -> None:
        self.model = None
        if Model:
            try:
                self.model = Model(lang="en-us")
            except Exception:
                self.model = None

    def transcribe(self, audio_base64: str, lang: str = "en") -> Tuple[str, float]:
        """Return transcription text and a rough confidence score."""

        audio_bytes = base64.b64decode(audio_base64)
        if not self.model or not KaldiRecognizer:
            return ("Transcription unavailable (model not installed)", 0.0)
        recognizer = KaldiRecognizer(self.model, 16000)
        recognizer.AcceptWaveform(audio_bytes)
        result_json = recognizer.Result()
        try:
            result = json.loads(result_json)
            text = result.get("text", "")
        except Exception:
            text = ""
        return text or "", 0.65 if text else 0.0
