from __future__ import annotations

import json
from typing import Any, Protocol

import httpx
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from genai_service.mcp_server import mcp
from genai_service.schemas import (
    ChatMessage,
    GenerateChatAnswerRequest,
    JsonBoard,
    JsonCandidateBoard,
)
from genai_service.settings import Settings


class AssistantError(RuntimeError):
    pass


class AssistantInfrastructureError(AssistantError):
    """Raised when an LLM or MCP dependency is unavailable."""


class SudokuAssistant(Protocol):
    async def answer(
        self,
        request: GenerateChatAnswerRequest,
        history: list[ChatMessage],
        solution: JsonBoard,
        template: JsonBoard,
        board: JsonBoard,
        candidates: JsonCandidateBoard,
    ) -> str:
        pass


class LangChainSudokuAssistant:
    _MAX_TOOL_ROUNDS = 6

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
        solution: JsonBoard,
        template: JsonBoard,
        board: JsonBoard,
        candidates: JsonCandidateBoard,
    ) -> str:
        messages = self._build_messages(
            request, history, solution, template, board, candidates
        )

        if self._chat_model is not None:
            try:
                response = await self._answer_with_model(messages)
            except AssistantInfrastructureError:
                return await self._answer_with_mcp_fallback(board, candidates, solution)
            if response:
                return response
            raise AssistantError("Assistant returned an empty response.")

        return await self._answer_with_mcp_fallback(board, candidates, solution)

    def _build_messages(
        self,
        request: GenerateChatAnswerRequest,
        history: list[ChatMessage],
        solution: JsonBoard,
        template: JsonBoard,
        board: JsonBoard,
        candidates: JsonCandidateBoard,
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

        for message in history[-10:]:
            if message.role == "assistant":
                messages.append(AIMessage(content=message.content))
            else:
                messages.append(HumanMessage(content=message.content))

        state = {
            "board": board,
            "template": template,
            "solution": solution,
            "candidates": candidates,
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
            if model is None:
                raise AssistantError("No model provided")
            if tools and hasattr(model, "bind_tools"):
                model = model.bind_tools(tools)

            tools_by_name = {tool.name: tool for tool in tools}
            for _ in range(self._MAX_TOOL_ROUNDS):
                try:
                    response = await model.ainvoke(messages)
                except Exception as exc:
                    if self._is_infrastructure_error(exc):
                        raise AssistantInfrastructureError(
                            "Language model is unavailable."
                        ) from exc
                    raise AssistantError("Language model request failed.") from exc
                tool_calls = getattr(response, "tool_calls", [])
                if not tool_calls:
                    return self._response_content(response)

                messages.append(response)
                for tool_call in tool_calls:
                    tool_name = tool_call["name"]
                    tool = tools_by_name.get(tool_name)
                    if tool is None:
                        raise AssistantError(
                            f"Model requested unknown Sudoku tool: {tool_name}."
                        )

                    result = await tool.ainvoke(tool_call["args"])
                    messages.append(
                        ToolMessage(
                            content=json.dumps(result, default=str),
                            tool_call_id=tool_call["id"],
                        )
                    )
        except Exception as exc:
            if isinstance(exc, AssistantError):
                raise
            if self._is_infrastructure_error(exc):
                raise AssistantInfrastructureError(
                    "Sudoku MCP service is unavailable."
                ) from exc
            raise AssistantError("Assistant orchestration failed.") from exc

        raise AssistantError("Assistant reached the maximum number of tool rounds.")

    @staticmethod
    def _is_infrastructure_error(exc: Exception) -> bool:
        """Recognize transport failures without masking agent or tool errors."""
        current: BaseException | None = exc
        while current is not None:
            if isinstance(current, httpx.HTTPStatusError):
                status_code = current.response.status_code
                if status_code == 408 or status_code == 429 or status_code >= 500:
                    return True
            elif isinstance(
                current,
                (httpx.TransportError, OSError, TimeoutError),
            ):
                return True
            status_code = getattr(current, "status_code", None)
            if status_code == 408 or status_code == 429 or (
                isinstance(status_code, int) and status_code >= 500
            ):
                return True
            if type(current).__name__ in {
                "APIConnectionError",
                "APITimeoutError",
                "InternalServerError",
                "ServiceUnavailableError",
            }:
                return True
            current = current.__cause__ or current.__context__
        return False

    @staticmethod
    def _response_content(response: Any) -> str:
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
        board: JsonBoard,
        candidates: JsonCandidateBoard,
        solution: JsonBoard,
    ) -> str:
        try:
            result = await mcp.call_tool(
                "find_next_step",
                {
                    "board": board,
                    "solution": solution,
                    "candidate_board": candidates,
                },
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

        if deleted_cells := next_step.get("deleted_cells"):
            row, col, value = deleted_cells[0]
            return (
                f"Der Eintrag {value} in Zeile {row + 1}, Spalte {col + 1} ist "
                "nicht korrekt und muss entfernt werden."
            )

        if deleted_candidates := next_step.get("deleted_candidates"):
            row, col, value = deleted_candidates[0]
            return (
                f"Die Kandidaten sind nicht konsistent: Kandidat {value} muss aus "
                f"Zeile {row + 1}, Spalte {col + 1} entfernt werden."
            )

        if missing_candidates := next_step.get("missing_candidates"):
            row, col, value = missing_candidates[0]
            return (
                f"Die Kandidaten sind nicht vollstaendig: Kandidat {value} fehlt in "
                f"Zeile {row + 1}, Spalte {col + 1}."
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
