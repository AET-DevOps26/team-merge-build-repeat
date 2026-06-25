from __future__ import annotations

from typing import List, NewType, Set, Tuple

Board = List[List[int]]
CandidateBoard = List[List[Set[int]]]
ValidatedBoard = NewType("ValidatedBoard", Board)
SolutionBoard = NewType("SolutionBoard", Board)
PartialValidatedCandidateBoard = NewType("PartialValidatedCandidateBoard", CandidateBoard)
ValidatedCandidateBoard = NewType("ValidatedCandidateBoard", CandidateBoard)
DeletedCell = Tuple[int, int, int]
DeletedCandidate = Tuple[int, int, int]
MissingCandidate = Tuple[int, int, int]


def _validate_board_shape(board: Board) -> None:
    """Ensure the board is a 9x9 grid."""
    if len(board) != 9:
        raise ValueError(f"Board must have 9 rows, got {len(board)}.")

    for row_index, row in enumerate(board):
        if len(row) != 9:
            raise ValueError(
                f"Row {row_index} must have 9 columns, got {len(row)}."
            )


def _validate_candidate_board_shape(candidate_board: CandidateBoard) -> None:
    """Ensure the candidate board is a 9x9 grid of sets."""
    if len(candidate_board) != 9:
        raise ValueError(
            f"Candidate board must have 9 rows, got {len(candidate_board)}."
        )

    for row_index, row in enumerate(candidate_board):
        if len(row) != 9:
            raise ValueError(
                f"Candidate row {row_index} must have 9 columns, got {len(row)}."
            )

        for col_index, candidates in enumerate(row):
            if not isinstance(candidates, set):
                raise TypeError(
                    "Candidate board entries must be sets, "
                    f"got {type(candidates).__name__} at ({row_index}, {col_index})."
                )


def _collect_forbidden_values(board: Board, row: int, col: int) -> set[int]:
    """Collect values already used in the row, column, and 3x3 box."""
    forbidden: set[int] = set()

    forbidden.update(value for value in board[row] if value != 0)
    forbidden.update(
        board[r][col]
        for r in range(9)
        if board[r][col] != 0
    )

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            value = board[r][c]
            if value != 0:
                forbidden.add(value)

    return forbidden


def validate_board_against_solution(
    board: Board,
    solution: SolutionBoard,
) -> tuple[ValidatedBoard, list[DeletedCell]]:
    """
    Compare a Sudoku board with the solution and remove all wrong placements.

    Rules:
    - 9x9 board
    - 0 means empty cell
    - values are expected to be in the range 1..9
    - indexes are 0-based

    The function mutates `board` in place, replacing wrong values with 0.
    It returns the updated board and a list of deleted cells.
    Each deleted cell is stored as (row, col, value).
    """
    _validate_board_shape(board)
    _validate_board_shape(solution)

    deleted_cells: list[DeletedCell] = []

    for row in range(9):
        for col in range(9):
            current_value = board[row][col]

            if current_value == 0:
                continue

            if current_value != solution[row][col]:
                deleted_cells.append((row, col, current_value))
                board[row][col] = 0

    return ValidatedBoard(board), deleted_cells


def validate_candidates_against_board(
    board: ValidatedBoard,
    solution: SolutionBoard,
    candidate_board: CandidateBoard,
) -> tuple[
    ValidatedCandidateBoard,
    list[DeletedCandidate],
    list[MissingCandidate],
]:
    """
    Remove invalid candidates and report required candidates that are missing.

    A candidate is considered wrong if the value is already present in the
    same row, column, or 3x3 box of the current board. A candidate is missing
    when an empty cell does not contain its value from the solved board.

    The function mutates `candidate_board` in place and returns the updated
    board plus removed and missing candidates as (row, col, value).
    """

    _validate_board_shape(board)
    _validate_board_shape(solution)
    _validate_candidate_board_shape(candidate_board)

    deleted_candidates: list[DeletedCandidate] = []
    missing_candidates: list[MissingCandidate] = []

    _remove_candidates_from_set_cells(board, candidate_board)

    for row in range(9):
        for col in range(9):
            candidates = candidate_board[row][col]

            if board[row][col] != 0:
                continue

            if candidates:
                forbidden_values = _collect_forbidden_values(board, row, col)
                invalid_candidates = candidates.intersection(forbidden_values)

                for value in sorted(invalid_candidates):
                    deleted_candidates.append((row, col, value))

                candidates.difference_update(invalid_candidates)

            solution_value = solution[row][col]
            if solution_value != 0 and solution_value not in candidates:
                missing_candidates.append((row, col, solution_value))

    return (
        ValidatedCandidateBoard(candidate_board),
        deleted_candidates,
        missing_candidates,
    )

def _remove_candidates_from_set_cells(
    board: ValidatedBoard,
    candidate_board: CandidateBoard,
) -> PartialValidatedCandidateBoard:
    """Remove all candidates from cells that already contain a fixed value."""

    for row in range(9):
        for col in range(9):
            fixed_value = board[row][col]
            candidates = candidate_board[row][col]

            if fixed_value == 0 or not candidates:
                continue

            candidates.clear()

    return PartialValidatedCandidateBoard(candidate_board)
