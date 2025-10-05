"""Minimal localisation helper."""

from __future__ import annotations

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "voice_title": "Voice & Control",
        "push_to_talk": "Push to talk",
        "transcript": "Transcript",
    },
    "es": {
        "voice_title": "Voz y control",
        "push_to_talk": "Pulsa para hablar",
        "transcript": "Transcripción",
    },
}


def t(key: str, lang: str = "en") -> str:
    """Return a translated string if available."""

    table = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return table.get(key, key)
