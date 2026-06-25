from __future__ import annotations

from collections.abc import Iterable
from typing import Tuple

from sudoku_lib.validation import ValidatedCandidateBoard

SinglePosition = Tuple[int, int, int]
CellPosition = tuple[int, int]


def find_single_positions(
    candidate_board: ValidatedCandidateBoard,
) -> list[SinglePosition]:
    """
    Return all candidates that have only one possible position in a unit.

    A unit is a row, column, or 3x3 box. Each single position is returned as
    (row, col, value), using 0-based indexes.
    """

    single_positions: set[SinglePosition] = set()

    for row in range(9):
        single_positions.update(
            _find_single_positions_in_unit(
                candidate_board,
                ((row, col) for col in range(9)),
            )
        )

    for col in range(9):
        single_positions.update(
            _find_single_positions_in_unit(
                candidate_board,
                ((row, col) for row in range(9)),
            )
        )

    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            single_positions.update(
                _find_single_positions_in_unit(
                    candidate_board,
                    (
                        (row, col)
                        for row in range(box_row, box_row + 3)
                        for col in range(box_col, box_col + 3)
                    ),
                )
            )

    return sorted(single_positions)


def _find_single_positions_in_unit(
    candidate_board: ValidatedCandidateBoard,
    positions: Iterable[CellPosition],
) -> list[SinglePosition]:
    candidates_by_value: dict[int, list[CellPosition]] = {
        value: [] for value in range(1, 10)
    }

    for row, col in positions:
        for value in candidate_board[row][col]:
            candidates_by_value[value].append((row, col))

    single_positions: list[SinglePosition] = []

    for value, value_positions in candidates_by_value.items():
        if len(value_positions) != 1:
            continue

        row, col = value_positions[0]
        single_positions.append((row, col, value))

    return single_positions
