from __future__ import annotations

from itertools import combinations

from sudoku_lib.strategy.common import (
    CandidateRemoval,
    CellPosition,
    StrategyReason,
    aligned_result,
    all_unit_positions,
    candidate_positions,
)
from sudoku_lib.validation import ValidatedCandidateBoard

SubsetRemoval = CandidateRemoval
SubsetReason = StrategyReason


def find_naked_pairs(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    return _find_naked_subset(candidate_board, 2)


def find_naked_triples(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    return _find_naked_subset(candidate_board, 3)


def find_naked_quads(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    return _find_naked_subset(candidate_board, 4)


def find_hidden_pairs(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    return _find_hidden_subset(candidate_board, 2)


def find_hidden_triples(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    return _find_hidden_subset(candidate_board, 3)


def find_hidden_quads(
    candidate_board: ValidatedCandidateBoard,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    return _find_hidden_subset(candidate_board, 4)


def _find_naked_subset(
    candidate_board: ValidatedCandidateBoard,
    size: int,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    removal_reasons: dict[CandidateRemoval, StrategyReason] = {}

    for unit in all_unit_positions():
        eligible_positions = [
            position
            for position in unit
            if 2 <= len(candidate_board[position[0]][position[1]]) <= size
        ]

        for subset_positions in combinations(eligible_positions, size):
            subset_values: set[int] = set()
            for row, col in subset_positions:
                subset_values.update(candidate_board[row][col])

            if len(subset_values) != size:
                continue

            matching_positions = {
                position
                for position in unit
                if candidate_board[position[0]][position[1]]
                and candidate_board[position[0]][position[1]].issubset(subset_values)
            }
            if matching_positions != set(subset_positions):
                continue

            reason = tuple(sorted(subset_positions))
            for row, col in unit:
                if (row, col) in matching_positions:
                    continue

                for value in sorted(candidate_board[row][col].intersection(subset_values)):
                    removal_reasons.setdefault((row, col, value), reason)

    return aligned_result(removal_reasons)


def _find_hidden_subset(
    candidate_board: ValidatedCandidateBoard,
    size: int,
) -> tuple[list[SubsetRemoval], list[SubsetReason]]:
    removal_reasons: dict[CandidateRemoval, StrategyReason] = {}

    for unit in all_unit_positions():
        positions_by_value = {
            value: candidate_positions(candidate_board, unit, value)
            for value in range(1, 10)
        }

        for values in combinations(range(1, 10), size):
            selected_positions: set[CellPosition] = set()

            for value in values:
                if len(positions_by_value[value]) < 2:
                    break

                selected_positions.update(positions_by_value[value])
            else:
                if len(selected_positions) != size:
                    continue

                reason = tuple(sorted(selected_positions))
                hidden_values = set(values)

                for row, col in selected_positions:
                    for value in sorted(candidate_board[row][col] - hidden_values):
                        removal_reasons.setdefault((row, col, value), reason)

    return aligned_result(removal_reasons)
