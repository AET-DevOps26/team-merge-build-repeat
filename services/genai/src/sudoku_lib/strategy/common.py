from __future__ import annotations

from sudoku_lib.validation import ValidatedCandidateBoard

CellPosition = tuple[int, int]
CandidateRemoval = tuple[int, int, int]
StrategyReason = tuple[CellPosition, ...]


def row_positions(row: int) -> tuple[CellPosition, ...]:
    return tuple((row, col) for col in range(9))


def col_positions(col: int) -> tuple[CellPosition, ...]:
    return tuple((row, col) for row in range(9))


def box_positions(box_row: int, box_col: int) -> tuple[CellPosition, ...]:
    return tuple(
        (row, col)
        for row in range(box_row, box_row + 3)
        for col in range(box_col, box_col + 3)
    )


def all_unit_positions() -> tuple[tuple[CellPosition, ...], ...]:
    return (
        *(row_positions(row) for row in range(9)),
        *(col_positions(col) for col in range(9)),
        *(
            box_positions(box_row, box_col)
            for box_row in range(0, 9, 3)
            for box_col in range(0, 9, 3)
        ),
    )


def candidate_positions(
    candidate_board: ValidatedCandidateBoard,
    positions: tuple[CellPosition, ...],
    value: int,
) -> list[CellPosition]:
    return [
        (row, col)
        for row, col in positions
        if value in candidate_board[row][col]
    ]


def aligned_result(
    removal_reasons: dict[CandidateRemoval, StrategyReason],
) -> tuple[list[CandidateRemoval], list[StrategyReason]]:
    removals = sorted(removal_reasons)
    reasons = [removal_reasons[removal] for removal in removals]

    return removals, reasons
