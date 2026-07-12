from __future__ import annotations

import json
import logging
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


logger = logging.getLogger("genai_service.assistant")


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
        logger.debug(
            "Prepared assistant context: history_messages=%d, prompt_messages=%d.",
            len(history),
            len(messages),
        )

        if self._chat_model is not None:
            try:
                response = await self._answer_with_model(messages)
            except AssistantInfrastructureError:
                logger.debug("Model infrastructure is unavailable; using MCP fallback.")
                return await self._answer_with_mcp_fallback(board, candidates, solution)
            if response:
                return response
            logger.debug("Model completed without a final text response.")
            raise AssistantError("Assistant returned an empty response.")

        logger.debug("No chat model is configured; using MCP fallback.")
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
            logger.debug(
                "Loaded %d MCP tools: %s.",
                len(tools),
                ", ".join(tool.name for tool in tools) or "none",
            )
            model = self._chat_model
            if model is None:
                raise AssistantError("No model provided")
            if tools and hasattr(model, "bind_tools"):
                model = model.bind_tools(tools)

            tools_by_name = {tool.name: tool for tool in tools}
            for round_number in range(1, self._MAX_TOOL_ROUNDS + 1):
                try:
                    logger.debug(
                        "Requesting model response: tool_round=%d, message_count=%d.",
                        round_number,
                        len(messages),
                    )
                    response = await model.ainvoke(messages)
                except Exception as exc:
                    if self._is_infrastructure_error(exc):
                        raise AssistantInfrastructureError(
                            "Language model is unavailable."
                        ) from exc
                    raise AssistantError("Language model request failed.") from exc
                tool_calls = getattr(response, "tool_calls", []) or []
                content = self._response_content(response)
                logger.debug(
                    "Received model response: tool_round=%d, content_length=%d, "
                    "tool_call_count=%d, tool_names=%s, finish_reason=%s.",
                    round_number,
                    len(content),
                    len(tool_calls),
                    ", ".join(
                        str(tool_call.get("name", "unknown"))
                        for tool_call in tool_calls
                        if isinstance(tool_call, dict)
                    )
                    or "none",
                    self._finish_reason(response),
                )
                logger.debug(
                    "Model response parser diagnostics: invalid_tool_call_count=%d, "
                    "invalid_tool_call_fields=%s, additional_kwarg_keys=%s, "
                    "additional_kwarg_shapes=%s, response_metadata_keys=%s.",
                    len(getattr(response, "invalid_tool_calls", []) or []),
                    self._field_sets(
                        getattr(response, "invalid_tool_calls", []) or []
                    ),
                    self._mapping_keys(getattr(response, "additional_kwargs", {})),
                    self._mapping_shapes(
                        getattr(response, "additional_kwargs", {})
                    ),
                    self._mapping_keys(getattr(response, "response_metadata", {})),
                )
                if not tool_calls:
                    return content

                messages.append(response)
                for tool_call in tool_calls:
                    tool_name = tool_call["name"]
                    tool = tools_by_name.get(tool_name)
                    if tool is None:
                        raise AssistantError(
                            f"Model requested unknown Sudoku tool: {tool_name}."
                        )

                    arguments = tool_call["args"]
                    logger.debug(
                        "Invoking MCP tool: name=%s, argument_keys=%s.",
                        tool_name,
                        self._argument_keys(arguments),
                    )
                    result = await tool.ainvoke(tool_call["args"])
                    logger.debug(
                        "MCP tool completed: name=%s, result_type=%s, result_keys=%s.",
                        tool_name,
                        type(result).__name__,
                        self._result_keys(result),
                    )
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
    def _finish_reason(response: Any) -> str:
        metadata = getattr(response, "response_metadata", {})
        if not isinstance(metadata, dict):
            return "unknown"
        return str(metadata.get("finish_reason", metadata.get("stop_reason", "unknown")))

    @staticmethod
    def _argument_keys(arguments: Any) -> str:
        if isinstance(arguments, dict):
            return ", ".join(sorted(str(key) for key in arguments)) or "none"
        return "non-object"

    @staticmethod
    def _result_keys(result: Any) -> str:
        if isinstance(result, dict):
            return ", ".join(sorted(str(key) for key in result)) or "none"
        return "not-applicable"

    @staticmethod
    def _mapping_keys(value: Any) -> str:
        if not isinstance(value, dict):
            return "not-a-mapping"
        return ", ".join(sorted(str(key) for key in value)) or "none"

    @classmethod
    def _mapping_shapes(cls, value: Any) -> str:
        if not isinstance(value, dict):
            return "not-a-mapping"
        return "; ".join(
            f"{key}={cls._value_shape(item)}" for key, item in sorted(value.items())
        ) or "none"

    @staticmethod
    def _field_sets(values: list[Any]) -> str:
        field_sets = [
            ", ".join(sorted(str(key) for key in value))
            for value in values
            if isinstance(value, dict)
        ]
        return "; ".join(field_sets) or "none"

    @staticmethod
    def _value_shape(value: Any) -> str:
        if isinstance(value, dict):
            return f"object({', '.join(sorted(str(key) for key in value)) or 'empty'})"
        if isinstance(value, list):
            if value and isinstance(value[0], dict):
                fields = ", ".join(sorted(str(key) for key in value[0])) or "empty"
                return f"list[{len(value)}](object({fields}))"
            return f"list[{len(value)}]"
        return type(value).__name__

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
