"""Text-to-speech utilities using pyttsx3 when available."""

from __future__ import annotations

try:
    import pyttsx3  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyttsx3 = None


class TTSService:
    """Provide spoken feedback using a friendly 'professional butler' tone."""

    def __init__(self, voice_style: str = "professional_butler") -> None:
        self.voice_style = voice_style
        self.engine = None
        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 165)
                self.engine.setProperty("volume", 0.9)
            except Exception:
                self.engine = None

    def speak(self, text: str) -> bool:
        """Speak the provided text if pyttsx3 is installed."""

        if not self.engine:
            return False
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception:
            return False
