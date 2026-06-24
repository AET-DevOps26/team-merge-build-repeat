from __future__ import annotations

from langchain_openai import ChatOpenAI

from genai_service.main import _configure_chat_model
from genai_service.settings import Settings


def test_openai_provider_uses_langchain_chat_openai() -> None:
    settings = Settings(
        chat_service_url="http://chat-service",
        game_service_url="http://game-service",
        mcp_command="python",
        mcp_args=["-m", "genai_service.mcp_server"],
        llm_provider="openai",
        ollama_base_url="http://ollama",
        ollama_model="ignored",
        openai_base_url="https://openai.example/v1",
        openai_api_key="test-key",
        openai_model="gpt-4o-mini",
    )

    model = _configure_chat_model(settings, None)

    assert isinstance(model, ChatOpenAI)
    assert model.model_name == "gpt-4o-mini"
    assert str(model.openai_api_base) == "https://openai.example/v1"
    assert model.temperature == 0

