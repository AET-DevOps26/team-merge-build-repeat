from __future__ import annotations

from sudoku_lib.strategy.common import (
    CandidateRemoval,
    StrategyReason,
    aligned_result,
    box_positions,
    candidate_positions,
    col_positions,
    row_positions,
)
from sudoku_lib.validation import ValidatedCandidateBoard

MultipleLineRemoval = CandidateRemoval
MultipleLineReason = StrategyReason


def find_multiple_lines(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[MultipleLineRemoval], list[MultipleLineReason]]:
    """
    Return candidates removable by multiple lines plus their reasons.

    If all candidates for a value in a row or column are inside one 3x3 box,
    remove that value from the other cells of that box.
    """

    removal_reasons: dict[CandidateRemoval, StrategyReason] = {}

    for row in range(9):
        for value in range(1, 10):
            positions = candidate_positions(candidate_board, row_positions(row), value)

            if len(positions) < 2:
                continue

            box_cols = {col // 3 for _, col in positions}
            if len(box_cols) != 1:
                continue

            box_col = next(iter(box_cols)) * 3
            reason = tuple(sorted(positions))

            for remove_row, remove_col in box_positions((row // 3) * 3, box_col):
                if remove_row == row:
                    continue

                if value not in candidate_board[remove_row][remove_col]:
                    continue

                removal_reasons.setdefault((remove_row, remove_col, value), reason)

    for col in range(9):
        for value in range(1, 10):
            positions = candidate_positions(candidate_board, col_positions(col), value)

            if len(positions) < 2:
                continue

            box_rows = {row // 3 for row, _ in positions}
            if len(box_rows) != 1:
                continue

            box_row = next(iter(box_rows)) * 3
            reason = tuple(sorted(positions))

            for remove_row, remove_col in box_positions(box_row, (col // 3) * 3):
                if remove_col == col:
                    continue

                if value not in candidate_board[remove_row][remove_col]:
                    continue

                removal_reasons.setdefault((remove_row, remove_col, value), reason)

    return aligned_result(removal_reasons)
