from __future__ import annotations

import os
import shlex
import sys
from dataclasses import dataclass


def _read_secret(name: str) -> str:
    value = os.getenv(name, "")
    file_path = os.getenv(f"{name}_FILE", "")
    if value or not file_path:
        return value

    with open(file_path, encoding="utf-8") as secret_file:
        return secret_file.read().strip()


def _normalize_root_path(value: str) -> str:
    root_path = value.strip()
    if root_path == "/":
        return ""
    return root_path.rstrip("/")


@dataclass(frozen=True)
class Settings:
    root_path: str
    chat_service_url: str
    game_service_url: str
    mcp_command: str
    mcp_args: list[str]
    llm_provider: str
    ollama_base_url: str
    ollama_model: str
    openai_base_url: str
    openai_api_key: str
    openai_model: str


def load_settings() -> Settings:
    return Settings(
        root_path=_normalize_root_path(os.getenv("GENAI_ROOT_PATH", "")),
        chat_service_url=os.getenv("CHAT_SERVICE_URL", "http://localhost:8081"),
        game_service_url=os.getenv("GAME_SERVICE_URL", "http://localhost:8080"),
        mcp_command=os.getenv("GENAI_MCP_COMMAND", sys.executable),
        mcp_args=shlex.split(
            os.getenv("GENAI_MCP_ARGS", "-m genai_service.mcp_server")
        ),
        llm_provider=os.getenv("LLM_PROVIDER", "").strip().lower(),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "smollm2:135m"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_api_key=_read_secret("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "openai/gpt-oss-120b"),
    )
