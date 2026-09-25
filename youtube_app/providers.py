"""LLM and embedding providers used by the application."""

from __future__ import annotations

import json
from typing import Sequence

import requests
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

from .config import Settings


class OpenRouterEmbeddings(Embeddings):
    """Small LangChain adapter for OpenRouter's OpenAI-compatible embeddings API."""

    def __init__(self, model: str, api_key: str, base_url: str, timeout: float) -> None:
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        response = requests.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "input": list(texts)},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return [
            item["embedding"]
            if isinstance(item["embedding"], list)
            else json.loads(item["embedding"])
            for item in payload["data"]
        ]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text])[0]


def create_embeddings(settings: Settings) -> OpenRouterEmbeddings:
    """Create the configured embedding provider."""
    return OpenRouterEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        timeout=settings.request_timeout,
    )


def create_llm(settings: Settings) -> ChatOpenAI:
    """Create the configured OpenRouter chat model."""
    return ChatOpenAI(
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_model,
        temperature=0.2,
        max_retries=2,
        timeout=settings.request_timeout,
    )
