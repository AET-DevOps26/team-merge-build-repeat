from __future__ import annotations

from sudoku_lib.strategy import (
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
)
from sudoku_lib.validation import ValidatedCandidateBoard


def empty_candidate_board() -> list[list[set[int]]]:
    return [[set() for _ in range(9)] for _ in range(9)]


def full_candidate_board() -> list[list[set[int]]]:
    return [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]


def test_finds_all_single_candidates_in_row_order() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {5}
    candidate_board[0][1] = {1, 2}
    candidate_board[4][8] = {9}
    candidate_board[8][3] = {2}

    single_candidates = find_single_candidates(
        ValidatedCandidateBoard(candidate_board),
    )

    assert single_candidates == [(0, 0, 5), (4, 8, 9), (8, 3, 2)]


def test_ignores_empty_and_multi_candidate_cells() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[3][3] = {1, 4}

    single_candidates = find_single_candidates(
        ValidatedCandidateBoard(candidate_board),
    )

    assert single_candidates == []


def test_finds_single_positions_in_rows_columns_and_boxes() -> None:
    candidate_board = full_candidate_board()

    for col in range(9):
        if col != 4:
            candidate_board[0][col].remove(5)

    for row in range(9):
        if row != 3:
            candidate_board[row][7].remove(6)

    for row in range(3):
        for col in range(3):
            if (row, col) != (1, 1):
                candidate_board[row][col].remove(7)

    single_positions = find_single_positions(
        ValidatedCandidateBoard(candidate_board),
    )

    assert single_positions == [
        (0, 4, 5),
        (1, 1, 7),
        (3, 7, 6),
    ]


def test_deduplicates_single_positions_found_in_multiple_units() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {5}
    candidate_board[0][1] = {1}
    candidate_board[1][0] = {2}

    single_positions = find_single_positions(
        ValidatedCandidateBoard(candidate_board),
    )

    assert single_positions == [(0, 0, 5), (0, 1, 1), (1, 0, 2)]


def test_finds_candidate_lines_in_rows() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {4}
    candidate_board[0][2] = {4}
    candidate_board[0][4] = {4, 8}
    candidate_board[0][8] = {4}
    candidate_board[1][1] = {2}
    candidate_board[2][2] = {3}

    removals, reasons = find_candidate_lines(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == [(0, 4, 4), (0, 8, 4)]
    assert reasons == [
        ((0, 0), (0, 2)),
        ((0, 0), (0, 2)),
    ]


def test_finds_candidate_lines_in_columns() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][3] = {6}
    candidate_board[2][3] = {1, 6}
    candidate_board[4][3] = {6}
    candidate_board[8][3] = {6, 9}
    candidate_board[1][4] = {2}
    candidate_board[2][5] = {3}

    removals, reasons = find_candidate_lines(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == [(4, 3, 6), (8, 3, 6)]
    assert reasons == [
        ((0, 3), (2, 3)),
        ((0, 3), (2, 3)),
    ]


def test_ignores_single_box_position_as_candidate_line() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {7}
    candidate_board[0][3] = {7}

    removals, reasons = find_candidate_lines(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == []
    assert reasons == []


def test_finds_double_pairs_in_rows() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {5}
    candidate_board[1][2] = {5}
    candidate_board[0][3] = {5}
    candidate_board[1][5] = {5}
    candidate_board[0][6] = {5, 8}
    candidate_board[0][8] = {5}
    candidate_board[1][7] = {5}
    candidate_board[2][6] = {5}

    removals, reasons = find_double_pairs(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == [(0, 6, 5), (0, 8, 5), (1, 7, 5)]
    assert reasons == [
        ((0, 0), (0, 3), (1, 2), (1, 5)),
        ((0, 0), (0, 3), (1, 2), (1, 5)),
        ((0, 0), (0, 3), (1, 2), (1, 5)),
    ]


def test_finds_double_pairs_in_columns() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {7}
    candidate_board[2][1] = {7}
    candidate_board[3][0] = {7}
    candidate_board[5][1] = {7}
    candidate_board[6][0] = {7}
    candidate_board[7][1] = {7, 9}
    candidate_board[8][2] = {7}

    removals, reasons = find_double_pairs(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == [(6, 0, 7), (7, 1, 7)]
    assert reasons == [
        ((0, 0), (2, 1), (3, 0), (5, 1)),
        ((0, 0), (2, 1), (3, 0), (5, 1)),
    ]


def test_ignores_double_pair_when_box_uses_more_than_two_lines() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {3}
    candidate_board[1][1] = {3}
    candidate_board[0][3] = {3}
    candidate_board[1][4] = {3}
    candidate_board[2][5] = {3}
    candidate_board[0][6] = {3}

    removals, reasons = find_double_pairs(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == []
    assert reasons == []


def test_finds_multiple_lines_in_rows() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {4}
    candidate_board[0][2] = {4}
    candidate_board[1][0] = {4}
    candidate_board[2][1] = {4, 8}
    candidate_board[4][0] = {4}

    removals, reasons = find_multiple_lines(
        ValidatedCandidateBoard(candidate_board),
    )

    assert removals == [(1, 0, 4), (2, 1, 4)]
    assert reasons == [
        ((0, 0), (0, 2)),
        ((0, 0), (0, 2)),
    ]


def test_finds_naked_pairs_triples_and_quads() -> None:
    pair_board = empty_candidate_board()
    pair_board[0][0] = {1, 2}
    pair_board[0][1] = {1, 2}
    pair_board[0][4] = {1, 2, 9}

    removals, reasons = find_naked_pairs(ValidatedCandidateBoard(pair_board))

    assert removals == [(0, 4, 1), (0, 4, 2)]
    assert reasons == [((0, 0), (0, 1)), ((0, 0), (0, 1))]

    triple_board = empty_candidate_board()
    triple_board[1][0] = {1, 2}
    triple_board[1][1] = {1, 3}
    triple_board[1][2] = {2, 3}
    triple_board[1][5] = {1, 3, 8}

    removals, reasons = find_naked_triples(ValidatedCandidateBoard(triple_board))

    assert removals == [(1, 5, 1), (1, 5, 3)]
    assert reasons == [
        ((1, 0), (1, 1), (1, 2)),
        ((1, 0), (1, 1), (1, 2)),
    ]

    quad_board = empty_candidate_board()
    quad_board[2][0] = {1, 2}
    quad_board[2][1] = {2, 3}
    quad_board[2][2] = {3, 4}
    quad_board[2][3] = {1, 4}
    quad_board[2][8] = {1, 4, 9}

    removals, reasons = find_naked_quads(ValidatedCandidateBoard(quad_board))

    assert removals == [(2, 8, 1), (2, 8, 4)]
    assert reasons == [
        ((2, 0), (2, 1), (2, 2), (2, 3)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
    ]


def test_finds_hidden_pairs_triples_and_quads() -> None:
    pair_board = empty_candidate_board()
    pair_board[0][0] = {1, 2, 8}
    pair_board[0][1] = {1, 2, 9}
    pair_board[0][2] = {3, 4}

    removals, reasons = find_hidden_pairs(ValidatedCandidateBoard(pair_board))

    assert removals == [(0, 0, 8), (0, 1, 9)]
    assert reasons == [((0, 0), (0, 1)), ((0, 0), (0, 1))]

    triple_board = empty_candidate_board()
    triple_board[1][0] = {1, 2, 8}
    triple_board[1][1] = {1, 3, 9}
    triple_board[1][2] = {2, 3, 7}
    triple_board[1][3] = {4, 5}

    removals, reasons = find_hidden_triples(ValidatedCandidateBoard(triple_board))

    assert removals == [(1, 0, 8), (1, 1, 9), (1, 2, 7)]
    assert reasons == [
        ((1, 0), (1, 1), (1, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((1, 0), (1, 1), (1, 2)),
    ]

    quad_board = empty_candidate_board()
    quad_board[2][0] = {1, 2, 8}
    quad_board[2][1] = {1, 3, 9}
    quad_board[2][2] = {2, 4, 7}
    quad_board[2][3] = {3, 4, 6}
    quad_board[2][4] = {5, 8}

    removals, reasons = find_hidden_quads(ValidatedCandidateBoard(quad_board))

    assert removals == [(2, 0, 8), (2, 1, 9), (2, 2, 7), (2, 3, 6)]
    assert reasons == [
        ((2, 0), (2, 1), (2, 2), (2, 3)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
    ]


def test_finds_x_wings_and_swordfish() -> None:
    x_wing_board = empty_candidate_board()
    x_wing_board[0][1] = {5}
    x_wing_board[0][7] = {5}
    x_wing_board[4][1] = {5}
    x_wing_board[4][7] = {5}
    x_wing_board[2][1] = {5, 8}
    x_wing_board[8][7] = {5}

    removals, reasons = find_x_wings(ValidatedCandidateBoard(x_wing_board))

    assert removals == [(2, 1, 5), (8, 7, 5)]
    assert reasons == [
        ((0, 1), (0, 7), (4, 1), (4, 7)),
        ((0, 1), (0, 7), (4, 1), (4, 7)),
    ]

    swordfish_board = empty_candidate_board()
    swordfish_board[0][1] = {6}
    swordfish_board[0][4] = {6}
    swordfish_board[3][1] = {6}
    swordfish_board[3][7] = {6}
    swordfish_board[6][4] = {6}
    swordfish_board[6][7] = {6}
    swordfish_board[2][1] = {6}
    swordfish_board[8][4] = {6, 9}

    removals, reasons = find_swordfish(ValidatedCandidateBoard(swordfish_board))

    assert removals == [(2, 1, 6), (8, 4, 6)]
    assert reasons == [
        ((0, 1), (0, 4), (3, 1), (3, 7), (6, 4), (6, 7)),
        ((0, 1), (0, 4), (3, 1), (3, 7), (6, 4), (6, 7)),
    ]


def test_find_next_step_returns_first_easy_strategy() -> None:
    candidate_board = empty_candidate_board()
    candidate_board[0][0] = {5}
    candidate_board[0][1] = {1, 2}
    candidate_board[0][2] = {1, 2}
    candidate_board[0][4] = {1, 2, 9}

    next_step = find_next_step(ValidatedCandidateBoard(candidate_board))

    assert next_step == ("single_candidate", [(0, 0, 5)])


def test_find_next_step_skips_empty_easier_strategies() -> None:
    candidate_board = full_candidate_board()
    candidate_board[0][0] = {1, 2}
    candidate_board[0][1] = {1, 2}
    candidate_board[0][4] = {1, 2, 9}

    next_step = find_next_step(ValidatedCandidateBoard(candidate_board))

    assert next_step is not None

    strategy_type, result = next_step
    removals, reasons = result

    assert strategy_type == "naked_pairs"
    assert (0, 4, 1) in removals
    assert (0, 4, 2) in removals
    assert reasons[removals.index((0, 4, 1))] == ((0, 0), (0, 1))
    assert reasons[removals.index((0, 4, 2))] == ((0, 0), (0, 1))


def test_find_next_step_returns_none_without_applicable_strategy() -> None:
    candidate_board = empty_candidate_board()

    assert find_next_step(ValidatedCandidateBoard(candidate_board)) is None
