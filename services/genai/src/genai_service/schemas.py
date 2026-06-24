from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


JsonBoard = list[list[int]]
JsonCandidateBoard = list[list[list[int]]]


def _validate_grid_shape(value: list, name: str) -> None:
    if len(value) != 9:
        raise ValueError(f"{name} must have 9 rows.")

    for row_index, row in enumerate(value):
        if len(row) != 9:
            raise ValueError(f"{name} row {row_index} must have 9 columns.")


class GenerateChatAnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    game_id: UUID = Field(alias="gameId")
    board: JsonBoard
    candidates: JsonCandidateBoard
    message: str = Field(min_length=1, max_length=10000)

    @field_validator("board")
    @classmethod
    def validate_board(cls, board: JsonBoard) -> JsonBoard:
        _validate_grid_shape(board, "board")
        for row in board:
            for value in row:
                if value < 0 or value > 9:
                    raise ValueError("board values must be between 0 and 9.")
        return board

    @field_validator("candidates")
    @classmethod
    def validate_candidates(
        cls,
        candidates: JsonCandidateBoard,
    ) -> JsonCandidateBoard:
        _validate_grid_shape(candidates, "candidates")
        for row in candidates:
            for cell in row:
                for value in cell:
                    if value < 1 or value > 9:
                        raise ValueError("candidate values must be between 1 and 9.")
        return candidates


class GameSolutionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    game_id: UUID = Field(alias="gameId")
    solution: JsonBoard

    @field_validator("solution")
    @classmethod
    def validate_solution(cls, solution: JsonBoard) -> JsonBoard:
        _validate_grid_shape(solution, "solution")
        for row in solution:
            for value in row:
                if value < 0 or value > 9:
                    raise ValueError("solution values must be between 0 and 9.")
        return solution

class GenerateChatAnswerResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    game_id: UUID = Field(alias="gameId")
    message: str
    assistant_response: str = Field(alias="assistantResponse")


class ChatMessage(BaseModel):
    id: UUID
    game_id: UUID = Field(alias="gameId")
    role: Literal["user", "assistant"]
    content: str
    created_at: str = Field(alias="createdAt")


class ChatResponse(BaseModel):
    game_id: UUID = Field(alias="gameId")
    messages: list[ChatMessage]
