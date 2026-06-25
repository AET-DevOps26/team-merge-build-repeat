from __future__ import annotations

import asyncio

import pytest

from genai_service.mcp_server import (
    find_candidate_lines,
    find_double_pairs,
    find_hidden_pairs,
    find_hidden_quads,
    find_hidden_triples,
    find_multiple_lines,
    find_naked_pairs,
    find_naked_quads,
    find_naked_triples,
    find_next_step,
    find_single_candidates,
    find_single_positions,
    find_swordfish,
    find_x_wings,
    mcp,
    validate_board_against_solution,
    validate_candidates_against_board,
)


def empty_board() -> list[list[int]]:
    return [[0 for _ in range(9)] for _ in range(9)]


def empty_candidate_board() -> list[list[list[int]]]:
    return [[[] for _ in range(9)] for _ in range(9)]


def test_validate_board_against_solution_returns_json_and_does_not_mutate_input() -> None:
    board = empty_board()
    solution = empty_board()
    board[0][0] = 7
    solution[0][0] = 3

    result = validate_board_against_solution(board, solution)

    assert result == {
        "board": [[0, 0, 0, 0, 0, 0, 0, 0, 0], *empty_board()[1:]],
        "deleted_cells": [[0, 0, 7]],
    }
    assert board[0][0] == 7


def test_validate_candidates_against_board_returns_sorted_json_candidates() -> None:
    board = empty_board()
    board[0][0] = 5
    solution = empty_board()
    solution[0][0] = 5
    candidate_board = empty_candidate_board()
    candidate_board[0][1] = [6, 5, 1]

    result = validate_candidates_against_board(board, solution, candidate_board)

    assert result["candidate_board"][0][1] == [1, 6]
    assert result["deleted_candidates"] == [[0, 1, 5]]
    assert result["missing_candidates"] == []
    assert candidate_board[0][1] == [6, 5, 1]


def test_find_single_candidates_returns_json_placements() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = [5]
    candidate_board[4][8] = [9]

    result = find_single_candidates(empty_board(), empty_board(), candidate_board)

    assert result == {"placements": [[0, 0, 5], [4, 8, 9]]}


def test_find_candidate_lines_returns_json_removals_and_reasons() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = [4]
    candidate_board[0][2] = [4]
    candidate_board[0][4] = [4, 8]

    result = find_candidate_lines(empty_board(), empty_board(), candidate_board)

    assert result == {
        "removals": [[0, 4, 4]],
        "reasons": [[[0, 0], [0, 2]]],
    }


def test_find_next_step_returns_none_when_no_strategy_applies() -> None:
    assert find_next_step(empty_board(), empty_board(), empty_candidate_board()) is None


def test_find_next_step_serializes_strategy_result() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[2][3] = [8]

    result = find_next_step(empty_board(), empty_board(), candidate_board)

    assert result == {
        "strategy": "single_candidate",
        "result": {"placements": [[2, 3, 8]]},
    }


def test_mcp_server_registers_and_calls_sudoku_tools() -> None:
    async def run() -> None:
        tools = await mcp.list_tools()
        tool_names = {tool.name for tool in tools}

        assert {
            "validate_board_against_solution",
            "validate_candidates_against_board",
            "find_next_step",
            "find_swordfish",
        }.issubset(tool_names)

        result = await mcp.call_tool(
            "find_single_candidates",
            {
                "board": empty_board(),
                "solution": empty_board(),
                "candidate_board": empty_candidate_board(),
            },
        )

        assert result[1] == {"placements": []}

        next_step = await mcp.call_tool(
            "find_next_step",
            {
                "board": empty_board(),
                "solution": empty_board(),
                "candidate_board": empty_candidate_board(),
            },
        )

        assert next_step[1] == {"result": None}

    asyncio.run(run())


def test_invalid_candidate_shape_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="Invalid Sudoku input"):
        find_single_candidates(
            empty_board(),
            empty_board(),
            [[[] for _ in range(9)] for _ in range(8)],
        )


@pytest.mark.parametrize(
    "finder",
    [
        find_single_candidates,
        find_single_positions,
        find_candidate_lines,
        find_double_pairs,
        find_multiple_lines,
        find_naked_pairs,
        find_naked_triples,
        find_naked_quads,
        find_hidden_pairs,
        find_hidden_triples,
        find_hidden_quads,
        find_x_wings,
        find_swordfish,
    ],
)
def test_find_tools_return_candidate_validation_result_before_strategy(
    finder: object,
) -> None:
    board = empty_board()
    board[0][0] = 5
    solution = empty_board()
    solution[0][0] = 5
    candidate_board = empty_candidate_board()
    candidate_board[0][1] = [5, 6]

    result = finder(board, solution, candidate_board)  # type: ignore[operator]

    assert result == {
        "candidate_board": [
            [[], [6], [], [], [], [], [], [], []],
            *empty_candidate_board()[1:],
        ],
        "deleted_candidates": [[0, 1, 5]],
    }
    assert candidate_board[0][1] == [5, 6]


def test_find_next_step_returns_candidate_validation_result_before_strategy() -> None:
    board = empty_board()
    board[0][0] = 5
    solution = empty_board()
    solution[0][0] = 5
    candidate_board = empty_candidate_board()
    candidate_board[0][1] = [5, 6]

    result = find_next_step(board, solution, candidate_board)

    assert result == {
        "candidate_board": [
            [[], [6], [], [], [], [], [], [], []],
            *empty_candidate_board()[1:],
        ],
        "deleted_candidates": [[0, 1, 5]],
    }


@pytest.mark.parametrize(
    "finder",
    [
        find_single_candidates,
        find_single_positions,
        find_candidate_lines,
        find_double_pairs,
        find_multiple_lines,
        find_naked_pairs,
        find_naked_triples,
        find_naked_quads,
        find_hidden_pairs,
        find_hidden_triples,
        find_hidden_quads,
        find_x_wings,
        find_swordfish,
        find_next_step,
    ],
)
def test_find_tools_return_missing_solution_candidates_before_strategy(
    finder: object,
) -> None:
    solution = empty_board()
    solution[0][1] = 5
    candidate_board = empty_candidate_board()
    candidate_board[0][1] = [1, 2]

    result = finder(empty_board(), solution, candidate_board)  # type: ignore[operator]

    assert result == {
        "candidate_board": [
            [[], [1, 2], [], [], [], [], [], [], []],
            *empty_candidate_board()[1:],
        ],
        "missing_candidates": [[0, 1, 5]],
    }


@pytest.mark.parametrize(
    "finder",
    [
        find_single_candidates,
        find_single_positions,
        find_candidate_lines,
        find_double_pairs,
        find_multiple_lines,
        find_naked_pairs,
        find_naked_triples,
        find_naked_quads,
        find_hidden_pairs,
        find_hidden_triples,
        find_hidden_quads,
        find_x_wings,
        find_swordfish,
        find_next_step,
    ],
)
def test_find_tools_return_board_validation_result_before_candidates(
    finder: object,
) -> None:
    board = empty_board()
    solution = empty_board()
    board[0][0] = 5
    candidate_board = empty_candidate_board()
    candidate_board[0][1] = [5, 6]

    result = finder(board, solution, candidate_board)  # type: ignore[operator]

    assert result == {
        "board": empty_board(),
        "deleted_cells": [[0, 0, 5]],
    }
