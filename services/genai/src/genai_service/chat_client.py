from __future__ import annotations

from typing import Literal
from uuid import UUID

import httpx

from genai_service.schemas import ChatResponse


class ChatServiceError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ChatServiceClient:
    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 10.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
        )

    async def get_chat(self, game_id: UUID, authorization: str) -> ChatResponse:
        response = await self._request(
            "GET",
            f"/v1/chat/{game_id}",
            authorization=authorization,
        )
        return ChatResponse.model_validate(response.json())

    async def create_message(
        self,
        game_id: UUID,
        role: Literal["user", "assistant"],
        content: str,
        authorization: str,
    ) -> None:
        await self._request(
            "POST",
            f"/v1/chat/{game_id}/messages",
            authorization=authorization,
            json={"role": role, "content": content},
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        url: str,
        *,
        authorization: str,
        json: dict[str, str] | None = None,
    ) -> httpx.Response:
        try:
            response = await self._client.request(
                method,
                url,
                headers={"Authorization": authorization},
                json=json,
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            raise ChatServiceError(
                f"Chat service returned HTTP {exc.response.status_code}.",
                exc.response.status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise ChatServiceError("Chat service is unavailable.") from exc
