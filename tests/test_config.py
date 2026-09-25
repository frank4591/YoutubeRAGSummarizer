import pytest

import youtube_app.config as config
from youtube_app.config import Settings


def test_settings_require_api_key(monkeypatch):
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY is required"):
        Settings.from_env()


def test_settings_load_environment(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("RETRIEVAL_K", "3")
    settings = Settings.from_env()
    assert settings.openrouter_api_key == "test-key"
    assert settings.retrieval_k == 3
