from __future__ import annotations

import asyncio
import json
from typing import Any

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from genai_service.assistant import (
    AssistantError,
    AssistantInfrastructureError,
    LangChainSudokuAssistant,
)
from genai_service.schemas import GenerateChatAnswerRequest
from genai_service.settings import Settings


def settings() -> Settings:
    return Settings(
        root_path="",
        chat_service_url="http://chat",
        game_service_url="http://game",
        mcp_command="python",
        mcp_args=["-m", "genai_service.mcp_server"],
        llm_provider="ollama",
        ollama_base_url="http://ollama",
        ollama_model="test",
        openai_base_url="http://openai",
        openai_api_key="",
        openai_model="test",
    )


class FakeTool:
    name = "find_next_step"

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def ainvoke(self, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(arguments)
        return {"strategy": "single_candidate", "value": 5}


class FakeModel:
    def __init__(self) -> None:
        self.bound_tools: list[Any] = []
        self.calls: list[list[Any]] = []

    def bind_tools(self, tools: list[Any]) -> FakeModel:
        self.bound_tools = tools
        return self

    async def ainvoke(self, messages: list[Any]) -> AIMessage:
        self.calls.append(list(messages))
        if len(self.calls) == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "find_next_step",
                        "args": {"candidate_board": [[[]]]},
                        "id": "call-1",
                    }
                ],
            )
        return AIMessage(content="Setze 5 in Zeile 1, Spalte 1.")


def empty_board() -> list[list[int]]:
    return [[0 for _ in range(9)] for _ in range(9)]


def empty_candidates() -> list[list[list[int]]]:
    return [[[] for _ in range(9)] for _ in range(9)]


def test_prompt_contains_template_and_solution_for_local_validation_context() -> None:
    assistant = LangChainSudokuAssistant(settings())
    solution = empty_board()
    solution[0][0] = 5
    template = empty_board()
    template[0][0] = 5
    request = GenerateChatAnswerRequest.model_validate(
        {
            "gameId": "00000000-0000-0000-0000-000000000000",
            "board": empty_board(),
            "candidates": empty_candidates(),
            "message": "Was ist falsch?",
        }
    )

    messages = assistant._build_messages(request, [], solution, template)
    state_json = messages[-1].content.split("\n", maxsplit=1)[1]
    state = json.loads(state_json)

    assert state["template"] == template
    assert state["solution"] == solution


def test_model_loop_executes_mcp_tool_and_returns_follow_up_response() -> None:
    async def run() -> None:
        model = FakeModel()
        tool = FakeTool()
        assistant = LangChainSudokuAssistant(settings(), chat_model=model)

        async def load_tools() -> list[Any]:
            return [tool]

        assistant._load_mcp_tools = load_tools  # type: ignore[method-assign]

        response = await assistant._answer_with_model([HumanMessage(content="Help")])

        assert response == "Setze 5 in Zeile 1, Spalte 1."
        assert model.bound_tools == [tool]
        assert tool.calls == [{"candidate_board": [[[]]]}]
        assert len(model.calls) == 2
        assert isinstance(model.calls[1][-2], AIMessage)
        assert isinstance(model.calls[1][-1], ToolMessage)
        assert model.calls[1][-1].tool_call_id == "call-1"

    asyncio.run(run())


def test_blank_model_response_is_not_replaced_by_mcp_fallback() -> None:
    class BlankModel(FakeModel):
        async def ainvoke(self, messages: list[Any]) -> AIMessage:
            self.calls.append(list(messages))
            return AIMessage(content="   ")

    async def run() -> None:
        model = BlankModel()
        assistant = LangChainSudokuAssistant(settings(), chat_model=model)
        request = GenerateChatAnswerRequest.model_validate(
            {
                "gameId": "00000000-0000-0000-0000-000000000000",
                "board": empty_board(),
                "candidates": empty_candidates(),
                "message": "Was ist der naechste Schritt?",
            }
        )

        async def load_tools() -> list[Any]:
            return []

        async def fallback(
            fallback_request: GenerateChatAnswerRequest,
            solution: list[list[int]],
        ) -> str:
            assert fallback_request is request
            assert solution == empty_board()
            return "Fallback-Antwort"

        assistant._load_mcp_tools = load_tools  # type: ignore[method-assign]
        assistant._answer_with_mcp_fallback = fallback  # type: ignore[method-assign]

        with pytest.raises(AssistantError, match="empty response"):
            await assistant.answer(
                request,
                [],
                empty_board(),
                empty_board(),
            )

        assert len(model.calls) == 1

    asyncio.run(run())


def test_model_orchestration_error_is_not_replaced_by_mcp_fallback() -> None:
    async def run() -> None:
        assistant = LangChainSudokuAssistant(settings(), chat_model=FakeModel())
        request = GenerateChatAnswerRequest.model_validate(
            {
                "gameId": "00000000-0000-0000-0000-000000000000",
                "board": empty_board(),
                "candidates": empty_candidates(),
                "message": "Was ist der naechste Schritt?",
            }
        )

        async def answer_with_model(messages: list[Any]) -> str:
            raise AssistantError("Tool binding failed")

        async def fallback(
            fallback_request: GenerateChatAnswerRequest,
            solution: list[list[int]],
        ) -> str:
            assert fallback_request is request
            assert solution == empty_board()
            return "Fallback-Antwort"

        assistant._answer_with_model = answer_with_model  # type: ignore[method-assign]
        assistant._answer_with_mcp_fallback = fallback  # type: ignore[method-assign]

        with pytest.raises(AssistantError, match="Tool binding failed"):
            await assistant.answer(
                request,
                [],
                empty_board(),
                empty_board(),
            )

    asyncio.run(run())


def test_model_infrastructure_error_uses_mcp_fallback() -> None:
    async def run() -> None:
        assistant = LangChainSudokuAssistant(settings(), chat_model=FakeModel())
        request = GenerateChatAnswerRequest.model_validate(
            {
                "gameId": "00000000-0000-0000-0000-000000000000",
                "board": empty_board(),
                "candidates": empty_candidates(),
                "message": "Was ist der naechste Schritt?",
            }
        )

        async def answer_with_model(messages: list[Any]) -> str:
            raise AssistantInfrastructureError("Language model is unavailable")

        async def fallback(
            fallback_request: GenerateChatAnswerRequest,
            solution: list[list[int]],
        ) -> str:
            assert fallback_request is request
            assert solution == empty_board()
            return "Fallback-Antwort"

        assistant._answer_with_model = answer_with_model  # type: ignore[method-assign]
        assistant._answer_with_mcp_fallback = fallback  # type: ignore[method-assign]

        response = await assistant.answer(
            request,
            [],
            empty_board(),
            empty_board(),
        )

        assert response == "Fallback-Antwort"

    asyncio.run(run())


def test_model_loop_stops_after_maximum_tool_rounds() -> None:
    class ToolCallingModel(FakeModel):
        async def ainvoke(self, messages: list[Any]) -> AIMessage:
            self.calls.append(list(messages))
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "find_next_step",
                        "args": {},
                        "id": f"call-{len(self.calls)}",
                    }
                ],
            )

    async def run() -> None:
        model = ToolCallingModel()
        assistant = LangChainSudokuAssistant(settings(), chat_model=model)

        async def load_tools() -> list[Any]:
            return [FakeTool()]

        assistant._load_mcp_tools = load_tools  # type: ignore[method-assign]

        with pytest.raises(AssistantError, match="maximum number of tool rounds"):
            await assistant._answer_with_model([HumanMessage(content="Help")])

        assert len(model.calls) == assistant._MAX_TOOL_ROUNDS

    asyncio.run(run())


def test_tool_round_limit_is_not_replaced_by_mcp_fallback() -> None:
    class ToolCallingModel(FakeModel):
        async def ainvoke(self, messages: list[Any]) -> AIMessage:
            self.calls.append(list(messages))
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "find_next_step",
                        "args": {},
                        "id": f"call-{len(self.calls)}",
                    }
                ],
            )

    async def run() -> None:
        assistant = LangChainSudokuAssistant(
            settings(),
            chat_model=ToolCallingModel(),
        )
        request = GenerateChatAnswerRequest.model_validate(
            {
                "gameId": "00000000-0000-0000-0000-000000000000",
                "board": empty_board(),
                "candidates": empty_candidates(),
                "message": "Was ist der naechste Schritt?",
            }
        )

        async def load_tools() -> list[Any]:
            return [FakeTool()]

        async def fallback(
            fallback_request: GenerateChatAnswerRequest,
            solution: list[list[int]],
        ) -> str:
            pytest.fail("The MCP fallback must not handle agent loop errors.")

        assistant._load_mcp_tools = load_tools  # type: ignore[method-assign]
        assistant._answer_with_mcp_fallback = fallback  # type: ignore[method-assign]

        with pytest.raises(AssistantError, match="maximum number of tool rounds"):
            await assistant.answer(
                request,
                [],
                empty_board(),
                empty_board(),
            )

    asyncio.run(run())
