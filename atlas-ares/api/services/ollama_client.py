"""Lightweight client for the local Ollama server."""

from __future__ import annotations

from typing import Any, Dict

import requests
from fastapi import HTTPException, status

from ..config import settings


class OllamaClient:
    """Simple wrapper around the Ollama HTTP API."""

    def __init__(self, host: str | None = None) -> None:
        self.host = host or settings.ollama_host.rstrip("/")

    def chat(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Dict[str, Any]:
        """Send a chat completion request."""

        url = f"{self.host}/api/generate"
        payload = {
            "model": model or settings.default_chat_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
        except requests.RequestException as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ollama unavailable") from exc
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Ollama error")
        data = response.json()
        return {
            "model": payload["model"],
            "output": data.get("response", ""),
            "prompt_tokens": data.get("prompt_eval_count"),
            "completion_tokens": data.get("eval_count"),
        }


def get_client() -> OllamaClient:
    """Return a default Ollama client instance."""

    return OllamaClient()
