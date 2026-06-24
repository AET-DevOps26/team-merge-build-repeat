from __future__ import annotations

from itertools import combinations

from sudoku_lib.strategy.common import (
    CandidateRemoval,
    StrategyReason,
    aligned_result,
)
from sudoku_lib.validation import ValidatedCandidateBoard

FishRemoval = CandidateRemoval
FishReason = StrategyReason


def find_x_wings(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[FishRemoval], list[FishReason]]:
    return _find_fish(candidate_board, 2)


def find_swordfish(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[FishRemoval], list[FishReason]]:
    return _find_fish(candidate_board, 3)


def _find_fish(
    candidate_board: ValidatedCandidateBoard,
    size: int,
) -> tuple[list[FishRemoval], list[FishReason]]:
    removal_reasons: dict[CandidateRemoval, StrategyReason] = {}

    for value in range(1, 10):
        _add_row_based_fish_removals(candidate_board, removal_reasons, value, size)
        _add_col_based_fish_removals(candidate_board, removal_reasons, value, size)

    return aligned_result(removal_reasons)


def _add_row_based_fish_removals(
    candidate_board: ValidatedCandidateBoard,
    removal_reasons: dict[CandidateRemoval, StrategyReason],
    value: int,
    size: int,
) -> None:
    cols_by_row = {
        row: {col for col in range(9) if value in candidate_board[row][col]}
        for row in range(9)
    }
    eligible_rows = [
        row
        for row, cols in cols_by_row.items()
        if 2 <= len(cols) <= size
    ]

    for rows in combinations(eligible_rows, size):
        fish_cols: set[int] = set()
        for row in rows:
            fish_cols.update(cols_by_row[row])

        if len(fish_cols) != size:
            continue

        reason = _row_fish_reason(candidate_board, rows, fish_cols, value)

        for row in range(9):
            if row in rows:
                continue

            for col in fish_cols:
                if value not in candidate_board[row][col]:
                    continue

                removal_reasons.setdefault((row, col, value), reason)


def _add_col_based_fish_removals(
    candidate_board: ValidatedCandidateBoard,
    removal_reasons: dict[CandidateRemoval, StrategyReason],
    value: int,
    size: int,
) -> None:
    rows_by_col = {
        col: {row for row in range(9) if value in candidate_board[row][col]}
        for col in range(9)
    }
    eligible_cols = [
        col
        for col, rows in rows_by_col.items()
        if 2 <= len(rows) <= size
    ]

    for cols in combinations(eligible_cols, size):
        fish_rows: set[int] = set()
        for col in cols:
            fish_rows.update(rows_by_col[col])

        if len(fish_rows) != size:
            continue

        reason = _col_fish_reason(candidate_board, fish_rows, cols, value)

        for col in range(9):
            if col in cols:
                continue

            for row in fish_rows:
                if value not in candidate_board[row][col]:
                    continue

                removal_reasons.setdefault((row, col, value), reason)


def _row_fish_reason(
    candidate_board: ValidatedCandidateBoard,
    rows: tuple[int, ...],
    cols: set[int],
    value: int,
) -> StrategyReason:
    return tuple(
        sorted(
            (row, col)
            for row in rows
            for col in cols
            if value in candidate_board[row][col]
        )
    )


def _col_fish_reason(
    candidate_board: ValidatedCandidateBoard,
    rows: set[int],
    cols: tuple[int, ...],
    value: int,
) -> StrategyReason:
    return tuple(
        sorted(
            (row, col)
            for col in cols
            for row in rows
            if value in candidate_board[row][col]
        )
    )
