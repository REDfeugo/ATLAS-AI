"""Local-first LLM interactions."""

from __future__ import annotations

import time
from typing import Dict, List

try:
    from ollama import Client as OllamaClient
except ImportError:  # pragma: no cover - optional dependency
    OllamaClient = None  # type: ignore

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

from ..core.config import get_settings

settings = get_settings()


class RateLimiter:
    """Very small in-memory rate limiter per process."""

    def __init__(self, max_per_minute: int) -> None:
        self.max_per_minute = max_per_minute
        self.calls: List[float] = []

    def allow(self) -> bool:
        now = time.time()
        window_start = now - 60
        self.calls = [t for t in self.calls if t >= window_start]
        if len(self.calls) >= self.max_per_minute:
            return False
        self.calls.append(now)
        return True


class LLMService:
    """Interface with Ollama or OpenAI depending on availability."""

    def __init__(self) -> None:
        self.settings = settings
        self.rate_limiter = RateLimiter(settings.rate_limit_per_minute)
        self.ollama_client = (
            OllamaClient(host=settings.ollama_host) if OllamaClient else None
        )
        self.openai_client = OpenAI(api_key=settings.openai_api_key) if (
            settings.openai_api_key and OpenAI
        ) else None

    def _chat_ollama(self, message: str, history: List[Dict]) -> Dict:
        """Call the Ollama API for chat completions."""

        if not self.ollama_client:
            raise RuntimeError("Ollama client unavailable")
        response = self.ollama_client.chat(
            model=self.settings.model_name,
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in history]
            + [{"role": "user", "content": message}],
        )
        content = response["message"]["content"]
        return {"reply": content, "tokens": len(content.split()), "model_used": self.settings.model_name}

    def _chat_openai(self, message: str, history: List[Dict]) -> Dict:
        """Fallback to OpenAI Chat Completions."""

        if not self.openai_client:
            raise RuntimeError("OpenAI client unavailable")
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in history]
            + [{"role": "user", "content": message}],
        )
        reply = response.choices[0].message.content or ""
        tokens = getattr(response.usage, "total_tokens", 0)
        return {"reply": reply, "tokens": tokens, "model_used": "gpt-3.5-turbo"}

    def chat(self, message: str, history: List[Dict]) -> Dict:
        """Return a chat response from the available provider."""

        if not self.rate_limiter.allow():
            return {
                "reply": "Too many requests. Please wait a moment before sending another message.",
                "tokens": 0,
                "model_used": "rate-limited",
            }

        try:
            return self._chat_ollama(message, history)
        except Exception:
            if self.openai_client:
                return self._chat_openai(message, history)
            return {
                "reply": "Model unavailable. Install Ollama or provide an OPENAI_API_KEY.",
                "tokens": 0,
                "model_used": "unavailable",
            }

    def voice_to_text(self) -> Dict:
        """Very simple microphone capture placeholder."""

        try:
            import speech_recognition as sr  # type: ignore
        except Exception:  # pragma: no cover - optional dependency
            return {"transcript": None}

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            transcript = recognizer.recognize_google(audio)
        except Exception:
            transcript = None
        return {"transcript": transcript}
