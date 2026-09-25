"""Backward-compatible provider factory.

New code should import providers from `youtube_app.providers` and pass explicit
`Settings` values. These functions remain for older scripts that imported this
module directly.
"""

from youtube_app.config import Settings
from youtube_app.providers import OpenRouterEmbeddings, create_embeddings, create_llm


def get_openrouter_embedding() -> OpenRouterEmbeddings:
    """Return embeddings using the current environment configuration."""
    return create_embeddings(Settings.from_env())


def get_openrouter_llm():
    """Return the chat model using the current environment configuration."""
    return create_llm(Settings.from_env())


__all__ = ["OpenRouterEmbeddings", "get_openrouter_embedding", "get_openrouter_llm"]
