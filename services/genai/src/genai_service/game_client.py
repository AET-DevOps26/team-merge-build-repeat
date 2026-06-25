from __future__ import annotations

from uuid import UUID

import httpx

from genai_service.schemas import GameSolutionResponse, JsonBoard


class GameServiceError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class GameServiceClient:
    """Stub client for the service that owns Sudoku game solutions."""

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

    async def get_solution(self, game_id: UUID, authorization: str) -> JsonBoard:
        response = await self._request(
            "GET",
            f"/v1/games/{game_id}/solution",
            authorization=authorization,
        )
        return GameSolutionResponse.model_validate(response.json()).solution

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        url: str,
        *,
        authorization: str,
    ) -> httpx.Response:
        try:
            response = await self._client.request(
                method,
                url,
                headers={"Authorization": authorization},
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            raise GameServiceError(
                f"Game service returned HTTP {exc.response.status_code}.",
                exc.response.status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise GameServiceError("Game service is unavailable.") from exc
