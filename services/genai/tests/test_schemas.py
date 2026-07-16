from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from genai_service.schemas import GenerateChatAnswerRequest


def empty_board() -> list[list[int]]:
    return [[0 for _ in range(9)] for _ in range(9)]


def empty_candidates() -> list[list[list[int]]]:
    return [[[] for _ in range(9)] for _ in range(9)]


def test_generate_chat_answer_request_accepts_valid_payload() -> None:
    game_id = uuid4()

    request = GenerateChatAnswerRequest.model_validate(
        {
            "gameId": str(game_id),
                "message": "Was nun?",
        }
    )

    assert request.game_id == game_id


def test_generate_chat_answer_request_rejects_client_supplied_game_state() -> None:
    with pytest.raises(ValidationError):
        GenerateChatAnswerRequest.model_validate(
            {
                "gameId": str(uuid4()),
                "board": empty_board(),
                "message": "Was nun?",
            }
        )


def test_generate_chat_answer_request_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        GenerateChatAnswerRequest.model_validate(
            {
                "gameId": str(uuid4()),
                "candidates": empty_candidates(),
                "message": "Was nun?",
            }
        )
