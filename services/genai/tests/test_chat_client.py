from __future__ import annotations

import asyncio
from uuid import uuid4

import httpx

from genai_service.chat_client import ChatServiceClient, ChatServiceError


def test_chat_client_forwards_authorization_and_payloads() -> None:
    async def run() -> None:
        game_id = uuid4()
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.method == "GET":
                return httpx.Response(
                    200,
                    json={"gameId": str(game_id), "messages": []},
                )
            return httpx.Response(
                201,
                json={
                    "id": str(uuid4()),
                    "gameId": str(game_id),
                    "role": "user",
                    "content": "Hallo",
                    "createdAt": "2026-06-18T10:00:00Z",
                },
            )

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(
            base_url="http://chat-service",
            transport=transport,
        ) as http_client:
            client = ChatServiceClient("http://chat-service", client=http_client)

            chat = await client.get_chat(game_id, "Bearer abc")
            await client.create_message(game_id, "user", "Hallo", "Bearer abc")

        assert chat.game_id == game_id
        assert [request.headers["Authorization"] for request in requests] == [
            "Bearer abc",
            "Bearer abc",
        ]
        assert requests[1].read() == b'{"role":"user","content":"Hallo"}'

    asyncio.run(run())


def test_chat_client_maps_http_errors() -> None:
    async def run() -> None:
        transport = httpx.MockTransport(lambda request: httpx.Response(403))
        async with httpx.AsyncClient(
            base_url="http://chat-service",
            transport=transport,
        ) as http_client:
            client = ChatServiceClient("http://chat-service", client=http_client)

            try:
                await client.get_chat(uuid4(), "Bearer abc")
            except ChatServiceError as exc:
                assert exc.status_code == 403
            else:
                raise AssertionError("Expected ChatServiceError")

    asyncio.run(run())
