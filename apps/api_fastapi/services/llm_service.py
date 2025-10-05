"""LLM service bridging Ollama and OpenAI."""

from __future__ import annotations

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
from ..core.rate_limit import SlidingWindowRateLimiter

settings = get_settings()


class LLMService:
    """Interface with Ollama or OpenAI depending on availability."""

    def __init__(self) -> None:
        self.settings = settings
        self.rate_limiter = SlidingWindowRateLimiter(settings.rate_limit_per_minute)
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
        return {
            "reply": content,
            "tokens": len(content.split()),
            "model_used": self.settings.model_name,
        }

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

    def chat(self, message: str, history: List[Dict], mode: str | None = None) -> Dict:
        """Return a chat response from the available provider."""

        if not self.rate_limiter.allow("chat"):
            return {
                "reply": "Too many requests. Please wait a moment before sending another message.",
                "tokens": 0,
                "model_used": "rate-limited",
            }
        provider_order: List[str]
        if mode == "cloud":
            provider_order = ["openai", "ollama"]
        elif mode == "local":
            provider_order = ["ollama", "openai"]
        else:
            provider_order = ["ollama", "openai"]

        for provider in provider_order:
            try:
                if provider == "ollama":
                    return self._chat_ollama(message, history)
                if provider == "openai":
                    return self._chat_openai(message, history)
            except Exception:
                continue
        return {
            "reply": "Model unavailable. Install Ollama or provide an OPENAI_API_KEY.",
            "tokens": 0,
            "model_used": "unavailable",
        }
