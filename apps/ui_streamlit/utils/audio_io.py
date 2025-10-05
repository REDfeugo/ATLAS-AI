"""Audio helpers used by the voice page."""

from __future__ import annotations

import base64
from dataclasses import dataclass

import numpy as np
try:
    import sounddevice as sd
except Exception:  # pragma: no cover - optional dependency
    sd = None  # type: ignore

SAMPLE_RATE = 16000


@dataclass
class Recording:
    """Container for captured audio and metadata."""

    samples: np.ndarray
    sample_rate: int = SAMPLE_RATE

    def as_base64(self) -> str:
        """Encode the recording as base64 for API transport."""

        pcm = (self.samples * np.iinfo(np.int16).max).astype(np.int16)
        return base64.b64encode(pcm.tobytes()).decode("ascii")


def list_input_devices() -> list[str]:
    """Return human-friendly input device names."""

    if not sd:
        return []
    devices = sd.query_devices()
    return [device["name"] for device in devices if device["max_input_channels"] > 0]


def record(seconds: float = 4.0, device: int | None = None) -> Recording:
    """Capture audio from the selected microphone."""

    if not sd:
        raise RuntimeError("sounddevice not installed")
    samples = sd.rec(
        int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32", device=device
    )
    sd.wait()
    return Recording(samples=samples.flatten())
