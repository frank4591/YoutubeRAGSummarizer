"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the application."""

    openrouter_api_key: str
    openrouter_model: str = "openrouter/free"
    embedding_model: str = "liquid/lfm-2.5-embedding-350m:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    chunk_size: int = 800
    chunk_overlap: int = 120
    retrieval_k: int = 5
    request_timeout: float = 120.0
    host: str = "0.0.0.0"
    port: int = 7860
    share: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from `.env` and process environment values."""
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required")

        return cls(
            openrouter_api_key=api_key,
            openrouter_model=os.getenv("OPENROUTER_MODEL", cls.openrouter_model),
            embedding_model=os.getenv("OPENROUTER_EMBEDDING_MODEL", cls.embedding_model),
            openrouter_base_url=os.getenv("OPENROUTER_BASE_URL", cls.openrouter_base_url),
            chunk_size=_env_int("CHUNK_SIZE", cls.chunk_size),
            chunk_overlap=_env_int("CHUNK_OVERLAP", cls.chunk_overlap),
            retrieval_k=_env_int("RETRIEVAL_K", cls.retrieval_k),
            request_timeout=_env_float("REQUEST_TIMEOUT", cls.request_timeout),
            host=os.getenv("GRADIO_SERVER_NAME", cls.host),
            port=_env_int("GRADIO_SERVER_PORT", cls.port),
            share=_env_bool("GRADIO_SHARE", cls.share),
        )


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return default if value is None else int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value is None else float(value)


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    return default if value is None else value.lower() in {"1", "true", "yes", "on"}
