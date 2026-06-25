from __future__ import annotations

from sudoku_lib.validation import ValidatedCandidateBoard

CellPosition = tuple[int, int]
CandidateLineRemoval = tuple[int, int, int]
CandidateLineReason = tuple[CellPosition, ...]


def find_candidate_lines(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[CandidateLineRemoval], list[CandidateLineReason]]:
    """
    Return candidates removable by candidate lines plus their reasons.

    If all positions for a value inside a 3x3 box are in the same row or
    column, that value can be removed from the rest of that row or column
    outside the box. Return values are aligned by index:
    removals[i] is justified by reasons[i].
    """

    removal_reasons: dict[CandidateLineRemoval, CandidateLineReason] = {}

    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            for value in range(1, 10):
                value_positions = _candidate_positions_in_box(
                    candidate_board,
                    box_row,
                    box_col,
                    value,
                )

                if len(value_positions) < 2:
                    continue

                rows = {row for row, _ in value_positions}
                cols = {col for _, col in value_positions}
                reason = tuple(sorted(value_positions))

                if len(rows) == 1:
                    row = next(iter(rows))
                    _add_row_removals(
                        candidate_board,
                        removal_reasons,
                        row,
                        box_col,
                        value,
                        reason,
                    )

                if len(cols) == 1:
                    col = next(iter(cols))
                    _add_col_removals(
                        candidate_board,
                        removal_reasons,
                        box_row,
                        col,
                        value,
                        reason,
                    )

    removals = sorted(removal_reasons)
    reasons = [removal_reasons[removal] for removal in removals]

    return removals, reasons


def _candidate_positions_in_box(
    candidate_board: ValidatedCandidateBoard,
    box_row: int,
    box_col: int,
    value: int,
) -> list[CellPosition]:
    positions: list[CellPosition] = []

    for row in range(box_row, box_row + 3):
        for col in range(box_col, box_col + 3):
            if value in candidate_board[row][col]:
                positions.append((row, col))

    return positions


def _add_row_removals(
    candidate_board: ValidatedCandidateBoard,
    removal_reasons: dict[CandidateLineRemoval, CandidateLineReason],
    row: int,
    box_col: int,
    value: int,
    reason: CandidateLineReason,
) -> None:
    for col in range(9):
        if box_col <= col < box_col + 3:
            continue

        if value not in candidate_board[row][col]:
            continue

        removal_reasons.setdefault((row, col, value), reason)


def _add_col_removals(
    candidate_board: ValidatedCandidateBoard,
    removal_reasons: dict[CandidateLineRemoval, CandidateLineReason],
    box_row: int,
    col: int,
    value: int,
    reason: CandidateLineReason,
) -> None:
    for row in range(9):
        if box_row <= row < box_row + 3:
            continue

        if value not in candidate_board[row][col]:
            continue

        removal_reasons.setdefault((row, col, value), reason)
