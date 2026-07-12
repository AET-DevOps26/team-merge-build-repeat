from __future__ import annotations

from uuid import UUID

import httpx

from genai_service.schemas import (
    GameSolutionResponse,
    GameTemplateResponse,
    JsonBoard,
    JsonBoardResponse,
    JsonCandidateBoard,
    JsonCandidateBoardResponse,
)


class GameServiceError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class GameServiceClient:
    """HTTP client for the Application service that owns Sudoku game data."""

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
            f"games/{game_id}/solution",
            authorization=authorization,
        )
        data = response.json()
        if isinstance(data, list):
            return JsonBoardResponse.model_validate(data).root
        return GameSolutionResponse.model_validate(data).solution

    async def get_template(self, game_id: UUID, authorization: str) -> JsonBoard:
        response = await self._request(
            "GET",
            f"games/{game_id}/template",
            authorization=authorization,
        )
        data = response.json()
        if isinstance(data, list):
            return JsonBoardResponse.model_validate(data).root
        return GameTemplateResponse.model_validate(data).template

    async def get_state(self, game_id: UUID, authorization: str) -> JsonBoard:
        response = await self._request(
            "GET",
            f"games/{game_id}/state",
            authorization=authorization,
        )
        return JsonBoardResponse.model_validate(response.json()).root

    async def get_pencil_marks(
        self,
        game_id: UUID,
        authorization: str,
    ) -> JsonCandidateBoard:
        response = await self._request(
            "GET",
            f"games/{game_id}/pencil-marks",
            authorization=authorization,
        )
        return JsonCandidateBoardResponse.model_validate(response.json()).root

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
