from __future__ import annotations

import pytest

from sudoku_lib.validation import (
    validate_board_against_solution,
    validate_candidates_against_board,
)


def empty_board() -> list[list[int]]:
    return [[0 for _ in range(9)] for _ in range(9)]


def empty_candidate_board() -> list[list[set[int]]]:
    return [[set() for _ in range(9)] for _ in range(9)]


def test_removes_wrong_values_and_keeps_correct_values() -> None:
    board = empty_board()
    solution = empty_board()

    board[0][0] = 5
    board[0][1] = 7
    board[8][8] = 9
    solution[0][0] = 5
    solution[0][1] = 3
    solution[8][8] = 9

    validated_board, deleted_cells = validate_board_against_solution(
        board,
        solution,
    )

    assert validated_board is board
    assert deleted_cells == [(0, 1, 7)]
    assert board[0][0] == 5
    assert board[0][1] == 0
    assert board[8][8] == 9


def test_rejects_invalid_board_shape() -> None:
    with pytest.raises(ValueError):
        validate_board_against_solution([[0] * 9 for _ in range(8)], empty_board())


def test_rejects_invalid_solution_shape() -> None:
    with pytest.raises(ValueError):
        validate_board_against_solution(empty_board(), [[0] * 8 for _ in range(9)])


def test_removes_candidates_present_in_row_column_and_box() -> None:
    board = empty_board()
    board[0][0] = 5
    board[0][4] = 8
    board[4][0] = 7
    board[1][1] = 9

    candidate_board = empty_candidate_board()
    candidate_board[0][1] = {1, 5, 6}
    candidate_board[1][0] = {2, 7, 9}
    candidate_board[4][4] = {7, 8, 9}

    validated_candidates, deleted_candidates = validate_candidates_against_board(
        board,
        candidate_board,
    )

    assert validated_candidates is candidate_board
    assert deleted_candidates == [(0, 1, 5), (1, 0, 7), (1, 0, 9), (4, 4, 7), (4, 4, 8)]
    assert candidate_board[0][1] == {1, 6}
    assert candidate_board[1][0] == {2}
    assert candidate_board[4][4] == {9}


def test_clears_candidates_for_fixed_cells() -> None:
    board = empty_board()
    board[2][2] = 4

    candidate_board = empty_candidate_board()
    candidate_board[2][2] = {1, 2, 3}

    _, deleted_candidates = validate_candidates_against_board(board, candidate_board)

    assert deleted_candidates == []
    assert candidate_board[2][2] == set()


def test_ignores_candidates_in_already_fixed_cells() -> None:
    board = empty_board()
    board[0][0] = 5

    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {5, 6}

    _, deleted_candidates = validate_candidates_against_board(board, candidate_board)

    assert deleted_candidates == []
    assert candidate_board[0][0] == set()


def test_rejects_invalid_candidate_board_shape() -> None:
    board = empty_board()
    with pytest.raises(ValueError):
        validate_candidates_against_board(board, [[set()] * 9 for _ in range(8)])


def test_rejects_non_set_candidate_entries() -> None:
    board = empty_board()
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = [1, 2, 3]  # type: ignore[assignment]

    with pytest.raises(TypeError):
        validate_candidates_against_board(board, candidate_board)
