"""Tests for Alibaba DashScope OpenAI-compatible client."""

from __future__ import annotations

from src.ai.client import AliClient, create_ai_client
from src.models import AIConfig, AIProvider

import pytest


def _make_config(**overrides) -> AIConfig:
    defaults = {
        "provider": AIProvider.ALI,
        "model": "qwen-plus",
        "api_key_env": "DASHSCOPE_API_KEY",
        "temperature": 0.3,
        "max_tokens": 4096,
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


class TestAliClientInit:
    def test_creates_instance_with_valid_config(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
        client = AliClient(_make_config())
        assert client.model == "qwen-plus"
        assert client.max_tokens == 4096

    def test_raises_when_api_key_missing(self, monkeypatch):
        monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
        with pytest.raises(ValueError, match="Missing API key"):
            AliClient(_make_config())

    def test_uses_default_base_url(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
        client = AliClient(_make_config())
        assert str(client.client.base_url).rstrip("/").endswith(
            "dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def test_uses_custom_base_url(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
        client = AliClient(_make_config(base_url="https://proxy.example.com/v1"))
        assert "proxy.example.com" in str(client.client.base_url)


class TestFactoryFunction:
    def test_creates_ali_client(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
        config = _make_config()
        client = create_ai_client(config)
        assert isinstance(client, AliClient)

    def test_ali_provider_enum(self):
        assert AIProvider.ALI.value == "ali"

