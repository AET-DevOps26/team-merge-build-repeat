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
                json=empty_board(),
            )

        async with httpx.AsyncClient(
            base_url="http://game-service",
            transport=httpx.MockTransport(handler),
        ) as http_client:
            client = GameServiceClient("http://game-service", client=http_client)
            solution = await client.get_solution(game_id, "Bearer abc")

        assert solution == empty_board()
        assert requests[0].url.path == f"/games/{game_id}/solution"
        assert requests[0].headers["Authorization"] == "Bearer abc"

    asyncio.run(run())


def test_game_client_gets_template_with_authorization() -> None:
    async def run() -> None:
        game_id = uuid4()
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json={"gameId": str(game_id), "template": empty_board()},
            )

        async with httpx.AsyncClient(
            base_url="http://game-service",
            transport=httpx.MockTransport(handler),
        ) as http_client:
            client = GameServiceClient("http://game-service", client=http_client)
            template = await client.get_template(game_id, "Bearer abc")

        assert template == empty_board()
        assert requests[0].url.path == f"/games/{game_id}/template"
        assert requests[0].headers["Authorization"] == "Bearer abc"

    asyncio.run(run())


def test_game_client_preserves_base_url_context_path() -> None:
    async def run() -> None:
        game_id = uuid4()
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, json=empty_board())

        async with httpx.AsyncClient(
            base_url="http://game-service/application/",
            transport=httpx.MockTransport(handler),
        ) as http_client:
            client = GameServiceClient(
                "http://game-service/application",
                client=http_client,
            )
            await client.get_solution(game_id, "Bearer abc")

        assert requests[0].url.path == f"/application/games/{game_id}/solution"

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
