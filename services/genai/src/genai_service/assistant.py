from __future__ import annotations

import json
from typing import Any, Protocol

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from genai_service.mcp_server import mcp
from genai_service.schemas import ChatMessage, GenerateChatAnswerRequest
from genai_service.settings import Settings


class AssistantError(RuntimeError):
    pass


class SudokuAssistant(Protocol):
    async def answer(
        self,
        request: GenerateChatAnswerRequest,
        history: list[ChatMessage],
    ) -> str:
        pass


class LangChainSudokuAssistant:
    def __init__(
        self,
        settings: Settings,
        *,
        chat_model: Any | None = None,
    ) -> None:
        self._settings = settings
        self._chat_model = chat_model

    async def answer(
        self,
        request: GenerateChatAnswerRequest,
        history: list[ChatMessage],
    ) -> str:
        messages = self._build_messages(request, history)

        if self._chat_model is not None:
            return await self._answer_with_model(messages)

        return await self._answer_with_mcp_fallback(request)

    def _build_messages(
        self,
        request: GenerateChatAnswerRequest,
        history: list[ChatMessage],
    ) -> list[BaseMessage]:
        messages: list[BaseMessage] = [
            SystemMessage(
                content=(
                    "You are a Sudoku assistant. Answer the user's question using "
                    "the current board, candidates, chat history, and Sudoku MCP "
                    "tools. Be concise and explain the concrete next reasoning step."
                )
            )
        ]

        for message in history:
            if message.role == "assistant":
                messages.append(AIMessage(content=message.content))
            else:
                messages.append(HumanMessage(content=message.content))

        state = {
            "board": request.board,
            "candidates": request.candidates,
            "question": request.message,
        }
        messages.append(
            HumanMessage(
                content=(
                    "Current Sudoku state and question:\n"
                    f"{json.dumps(state, separators=(',', ':'))}"
                )
            )
        )
        return messages

    async def _answer_with_model(self, messages: list[BaseMessage]) -> str:
        try:
            tools = await self._load_mcp_tools()
            model = self._chat_model
            if tools and hasattr(model, "bind_tools"):
                model = model.bind_tools(tools)
            response = await model.ainvoke(messages)
        except Exception as exc:
            raise AssistantError("Assistant orchestration failed.") from exc

        content = getattr(response, "content", response)
        if isinstance(content, list):
            return " ".join(str(item) for item in content).strip()
        return str(content).strip()

    async def _load_mcp_tools(self) -> list[Any]:
        try:
            from langchain_mcp_adapters.client import MultiServerMCPClient
        except ImportError:
            return []

        client = MultiServerMCPClient(
            {
                "sudoku": {
                    "command": self._settings.mcp_command,
                    "args": self._settings.mcp_args,
                    "transport": "stdio",
                }
            }
        )
        return await client.get_tools()

    async def _answer_with_mcp_fallback(
        self,
        request: GenerateChatAnswerRequest,
    ) -> str:
        try:
            result = await mcp.call_tool(
                "find_next_step",
                {"candidate_board": request.candidates},
            )
        except Exception as exc:
            raise AssistantError("Sudoku MCP tool call failed.") from exc

        next_step = result[1].get("result")
        if next_step is None:
            return (
                "Ich finde mit den aktuellen Kandidaten keinen eindeutigen naechsten "
                "Sudoku-Schritt. Pruefe bitte zuerst, ob Board und Kandidaten "
                "vollstaendig und konsistent sind."
            )

        strategy = next_step["strategy"]
        strategy_result = next_step["result"]
        if placements := strategy_result.get("placements"):
            row, col, value = placements[0]
            return (
                f"Mit der Strategie {strategy} ist der naechste Schritt: "
                f"Setze {value} in Zeile {row + 1}, Spalte {col + 1}."
            )

        if removals := strategy_result.get("removals"):
            row, col, value = removals[0]
            return (
                f"Mit der Strategie {strategy} kannst du Kandidat {value} aus "
                f"Zeile {row + 1}, Spalte {col + 1} entfernen."
            )

        return (
            f"Die Strategie {strategy} ist anwendbar, aber es wurde kein konkreter "
            "Placement- oder Removal-Schritt zurueckgegeben."
        )
