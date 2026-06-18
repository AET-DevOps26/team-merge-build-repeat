from __future__ import annotations

from typing import Any

import httpx
from langchain_core.messages import AIMessage, BaseMessage


class OllamaChatModel:
    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        timeout: float = 120.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    async def ainvoke(self, messages: list[BaseMessage]) -> AIMessage:
        payload = {
            "model": self._model,
            "stream": False,
            "messages": [
                {"role": self._role_for(message), "content": str(message.content)}
                for message in messages
            ],
        }

        async with httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
        ) as client:
            response = await client.post("/api/chat", json=payload)
            response.raise_for_status()

        data: dict[str, Any] = response.json()
        content = data.get("message", {}).get("content", "")
        return AIMessage(content=content)

    def _role_for(self, message: BaseMessage) -> str:
        if message.type == "system":
            return "system"
        if message.type == "ai":
            return "assistant"
        return "user"
