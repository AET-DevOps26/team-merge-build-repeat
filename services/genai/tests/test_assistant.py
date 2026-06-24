from __future__ import annotations

import asyncio
from typing import Any

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from genai_service.assistant import AssistantError, LangChainSudokuAssistant
from genai_service.settings import Settings


def settings() -> Settings:
    return Settings(
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
