from __future__ import annotations

import asyncio
from uuid import UUID, uuid4

import httpx

from genai_service.assistant import AssistantError
from genai_service.main import create_app
from genai_service.schemas import ChatResponse, GenerateChatAnswerRequest


def empty_board() -> list[list[int]]:
    return [[0 for _ in range(9)] for _ in range(9)]


def empty_candidates() -> list[list[list[int]]]:
    return [[[] for _ in range(9)] for _ in range(9)]


class FakeChatClient:
    def __init__(self) -> None:
        self.created_messages: list[tuple[UUID, str, str, str]] = []
        self.authorization: str | None = None

    async def get_chat(self, game_id: UUID, authorization: str) -> ChatResponse:
        self.authorization = authorization
        return ChatResponse.model_validate(
            {
                "gameId": str(game_id),
                "messages": [
                    {
                        "id": str(uuid4()),
                        "gameId": str(game_id),
                        "role": "user",
                        "content": "Was war der letzte Schritt?",
                        "createdAt": "2026-06-18T10:00:00Z",
                    }
                ],
            }
        )

    async def create_message(
        self,
        game_id: UUID,
        role: str,
        content: str,
        authorization: str,
    ) -> None:
        self.created_messages.append((game_id, role, content, authorization))

    async def aclose(self) -> None:
        pass


class FakeAssistant:
    def __init__(self, response: str = "Setze 5 in Zeile 1, Spalte 1.") -> None:
        self.response = response
        self.history_size = 0

    async def answer(
        self,
        request: GenerateChatAnswerRequest,
        history: list,
    ) -> str:
        self.history_size = len(history)
        return self.response


class FailingAssistant:
    async def answer(
        self,
        request: GenerateChatAnswerRequest,
        history: list,
    ) -> str:
        raise AssistantError("Assistant orchestration failed.")


def test_answer_chat_uses_history_and_stores_user_and_assistant_messages() -> None:
    async def run() -> None:
        app = create_app()
        game_id = uuid4()
        chat_client = FakeChatClient()
        assistant = FakeAssistant()
        app.state.chat_client = chat_client
        app.state.assistant = assistant
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/v1/chat/answer",
                headers={"Authorization": "Bearer test-token"},
                json={
                    "gameId": str(game_id),
                    "board": empty_board(),
                    "candidates": empty_candidates(),
                    "message": "Was soll ich als naechstes tun?",
                },
            )

        assert response.status_code == 200
        assert response.json() == {
            "gameId": str(game_id),
            "message": "Was soll ich als naechstes tun?",
            "assistantResponse": "Setze 5 in Zeile 1, Spalte 1.",
        }
        assert chat_client.authorization == "Bearer test-token"
        assert assistant.history_size == 1
        assert chat_client.created_messages == [
            (
                game_id,
                "user",
                "Was soll ich als naechstes tun?",
                "Bearer test-token",
            ),
            (
                game_id,
                "assistant",
                "Setze 5 in Zeile 1, Spalte 1.",
                "Bearer test-token",
            ),
        ]

    asyncio.run(run())


def test_answer_chat_requires_bearer_auth() -> None:
    async def run() -> None:
        app = create_app()
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/v1/chat/answer",
                json={
                    "gameId": str(uuid4()),
                    "board": empty_board(),
                    "candidates": empty_candidates(),
                    "message": "Hilfe",
                },
            )

        assert response.status_code == 401

    asyncio.run(run())


def test_answer_chat_does_not_store_messages_when_assistant_fails() -> None:
    async def run() -> None:
        app = create_app()
        chat_client = FakeChatClient()
        app.state.chat_client = chat_client
        app.state.assistant = FailingAssistant()
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/v1/chat/answer",
                headers={"Authorization": "Bearer test-token"},
                json={
                    "gameId": str(uuid4()),
                    "board": empty_board(),
                    "candidates": empty_candidates(),
                    "message": "Hilfe",
                },
            )

        assert response.status_code == 503
        assert chat_client.created_messages == []

    asyncio.run(run())


def test_answer_chat_rejects_invalid_board_shape() -> None:
    async def run() -> None:
        app = create_app()
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/v1/chat/answer",
                headers={"Authorization": "Bearer test-token"},
                json={
                    "gameId": str(uuid4()),
                    "board": [[0 for _ in range(9)] for _ in range(8)],
                    "candidates": empty_candidates(),
                    "message": "Hilfe",
                },
            )

        assert response.status_code == 422

    asyncio.run(run())
