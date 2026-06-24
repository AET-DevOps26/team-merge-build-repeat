from __future__ import annotations

import asyncio
from uuid import uuid4

import httpx

from genai_service.game_client import GameServiceClient, GameServiceError


def empty_board() -> list[list[int]]:
    return [[0 for _ in range(9)] for _ in range(9)]


def test_game_client_gets_solution_with_authorization() -> None:
    async def run() -> None:
        game_id = uuid4()
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json={"gameId": str(game_id), "solution": empty_board()},
            )

        async with httpx.AsyncClient(
            base_url="http://game-service",
            transport=httpx.MockTransport(handler),
        ) as http_client:
            client = GameServiceClient("http://game-service", client=http_client)
            solution = await client.get_solution(game_id, "Bearer abc")

        assert solution == empty_board()
        assert requests[0].url.path == f"/v1/games/{game_id}/solution"
        assert requests[0].headers["Authorization"] == "Bearer abc"

    asyncio.run(run())


def test_game_client_maps_http_errors() -> None:
    async def run() -> None:
        async with httpx.AsyncClient(
            base_url="http://game-service",
            transport=httpx.MockTransport(lambda request: httpx.Response(404)),
        ) as http_client:
            client = GameServiceClient("http://game-service", client=http_client)
            try:
                await client.get_solution(uuid4(), "Bearer abc")
            except GameServiceError as exc:
                assert exc.status_code == 404
            else:
                raise AssertionError("Expected GameServiceError")

    asyncio.run(run())
