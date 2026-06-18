from __future__ import annotations

from itertools import combinations

from sudoku_lib.validation import ValidatedCandidateBoard

CellPosition = tuple[int, int]
DoublePairRemoval = tuple[int, int, int]
DoublePairReason = tuple[CellPosition, ...]


def find_double_pairs(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[DoublePairRemoval], list[DoublePairReason]]:
    """
    Return candidates removable by double pairs plus their reasons.

    In a horizontal band, if the same value is restricted to the same two rows
    in two boxes, remove it from those rows in the third box. The vertical
    stack case works the same way with columns. Return values are aligned by
    index: removals[i] is justified by reasons[i].
    """

    removal_reasons: dict[DoublePairRemoval, DoublePairReason] = {}

    for box_row in range(0, 9, 3):
        _add_double_pair_row_removals(candidate_board, removal_reasons, box_row)

    for box_col in range(0, 9, 3):
        _add_double_pair_col_removals(candidate_board, removal_reasons, box_col)

    removals = sorted(removal_reasons)
    reasons = [removal_reasons[removal] for removal in removals]

    return removals, reasons


def _add_double_pair_row_removals(
    candidate_board: ValidatedCandidateBoard,
    removal_reasons: dict[DoublePairRemoval, DoublePairReason],
    box_row: int,
) -> None:
    box_cols = (0, 3, 6)

    for value in range(1, 10):
        rows_by_box_col: dict[int, set[int]] = {}
        positions_by_box_col: dict[int, list[CellPosition]] = {}

        for box_col in box_cols:
            positions = _candidate_positions_in_box(
                candidate_board,
                box_row,
                box_col,
                value,
            )
            rows = {row for row, _ in positions}

            if len(rows) != 2:
                continue

            rows_by_box_col[box_col] = rows
            positions_by_box_col[box_col] = positions

        for first_box_col, second_box_col in combinations(rows_by_box_col, 2):
            if rows_by_box_col[first_box_col] != rows_by_box_col[second_box_col]:
                continue

            target_box_col = next(
                box_col
                for box_col in box_cols
                if box_col not in (first_box_col, second_box_col)
            )
            reason = tuple(
                sorted(
                    positions_by_box_col[first_box_col]
                    + positions_by_box_col[second_box_col]
                )
            )

            for row in sorted(rows_by_box_col[first_box_col]):
                for col in range(target_box_col, target_box_col + 3):
                    if value not in candidate_board[row][col]:
                        continue

                    removal_reasons.setdefault((row, col, value), reason)


def _add_double_pair_col_removals(
    candidate_board: ValidatedCandidateBoard,
    removal_reasons: dict[DoublePairRemoval, DoublePairReason],
    box_col: int,
) -> None:
    box_rows = (0, 3, 6)

    for value in range(1, 10):
        cols_by_box_row: dict[int, set[int]] = {}
        positions_by_box_row: dict[int, list[CellPosition]] = {}

        for box_row in box_rows:
            positions = _candidate_positions_in_box(
                candidate_board,
                box_row,
                box_col,
                value,
            )
            cols = {col for _, col in positions}

            if len(cols) != 2:
                continue

            cols_by_box_row[box_row] = cols
            positions_by_box_row[box_row] = positions

        for first_box_row, second_box_row in combinations(cols_by_box_row, 2):
            if cols_by_box_row[first_box_row] != cols_by_box_row[second_box_row]:
                continue

            target_box_row = next(
                box_row
                for box_row in box_rows
                if box_row not in (first_box_row, second_box_row)
            )
            reason = tuple(
                sorted(
                    positions_by_box_row[first_box_row]
                    + positions_by_box_row[second_box_row]
                )
            )

            for col in sorted(cols_by_box_row[first_box_row]):
                for row in range(target_box_row, target_box_row + 3):
                    if value not in candidate_board[row][col]:
                        continue

                    removal_reasons.setdefault((row, col, value), reason)


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
