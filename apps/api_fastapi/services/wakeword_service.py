"""Wake-word detection helpers."""

from __future__ import annotations

try:
    from openwakeword import Model  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    Model = None  # type: ignore


class WakeWordService:
    """Expose a simple API to check whether audio contains the wake word."""

    def __init__(self, wakeword: str) -> None:
        self.wakeword = wakeword
        self.model = None
        if Model:
            try:
                self.model = Model()
            except Exception:
                self.model = None

    def detect(self, audio_base64: str) -> bool:
        """Return True if the wake word was detected (stubbed offline)."""

        return False
