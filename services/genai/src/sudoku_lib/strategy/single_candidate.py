from __future__ import annotations

from typing import Tuple

from sudoku_lib.validation import ValidatedCandidateBoard

SingleCandidate = Tuple[int, int, int]


def find_single_candidates(
    candidate_board: ValidatedCandidateBoard,
) -> list[SingleCandidate]:
    """
    Return all cells that have exactly one remaining candidate.

    Each single candidate is returned as (row, col, value), using 0-based
    indexes. Results are ordered row by row.
    """

    single_candidates: list[SingleCandidate] = []

    for row in range(9):
        for col in range(9):
            candidates = candidate_board[row][col]

            if len(candidates) != 1:
                continue

            value = next(iter(candidates))
            single_candidates.append((row, col, value))

    return single_candidates
