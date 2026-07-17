from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeAlias

from mcp.server.fastmcp import FastMCP

from sudoku_lib import (
    ValidatedCandidateBoard,
    find_candidate_lines as sudoku_find_candidate_lines,
    find_double_pairs as sudoku_find_double_pairs,
    find_hidden_pairs as sudoku_find_hidden_pairs,
    find_hidden_quads as sudoku_find_hidden_quads,
    find_hidden_triples as sudoku_find_hidden_triples,
    find_multiple_lines as sudoku_find_multiple_lines,
    find_naked_pairs as sudoku_find_naked_pairs,
    find_naked_quads as sudoku_find_naked_quads,
    find_naked_triples as sudoku_find_naked_triples,
    find_next_step as sudoku_find_next_step,
    find_single_candidates as sudoku_find_single_candidates,
    find_single_positions as sudoku_find_single_positions,
    find_swordfish as sudoku_find_swordfish,
    find_x_wings as sudoku_find_x_wings,
    validate_board_against_solution as sudoku_validate_board_against_solution,
    validate_candidates_against_board as sudoku_validate_candidates_against_board,
)

JsonBoard: TypeAlias = list[list[int]]
JsonCandidateBoard: TypeAlias = list[list[list[int]]]
JsonObject: TypeAlias = dict[str, Any]
SingleStrategyFinder: TypeAlias = Callable[[ValidatedCandidateBoard], list[tuple[int, int, int]]]
RemovalStrategyFinder: TypeAlias = Callable[
    [ValidatedCandidateBoard],
    tuple[list[tuple[int, int, int]], list[tuple[tuple[int, int], ...]]],
]

mcp = FastMCP("Sudoku")


def _copy_board(board: JsonBoard) -> JsonBoard:
    return [list(row) for row in board]


def _validate_candidate_board_shape(candidate_board: JsonCandidateBoard) -> None:
    if len(candidate_board) != 9:
        raise ValueError(
            f"Candidate board must have 9 rows, got {len(candidate_board)}."
        )

    for row_index, row in enumerate(candidate_board):
        if len(row) != 9:
            raise ValueError(
                f"Candidate row {row_index} must have 9 columns, got {len(row)}."
            )


def _candidate_board_from_json(
    candidate_board: JsonCandidateBoard,
) -> ValidatedCandidateBoard:
    _validate_candidate_board_shape(candidate_board)

    return ValidatedCandidateBoard(
        [
            [set(candidates) for candidates in row]
            for row in candidate_board
        ]
    )


def _candidate_board_to_json(
    candidate_board: ValidatedCandidateBoard,
) -> JsonCandidateBoard:
    return [
        [sorted(candidates) for candidates in row]
        for row in candidate_board
    ]


def _jsonify(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonify(item) for item in value]

    if isinstance(value, list):
        return [_jsonify(item) for item in value]

    if isinstance(value, set):
        return sorted(value)

    return value


def _jsonify_cell_changes(changes: list[tuple[int, int, int]]) -> list[list[int]]:
    """Serialize cell changes with 1-based row and column coordinates."""

    return [[row + 1, col + 1, value] for row, col, value in changes]


def _jsonify_positions(
    reasons: list[tuple[tuple[int, int], ...]],
) -> list[list[list[int]]]:
    """Serialize cell positions with 1-based row and column coordinates."""

    return [
        [[row + 1, col + 1] for row, col in reason]
        for reason in reasons
    ]


def _run_with_input_errors(callback: Callable[[], JsonObject]) -> JsonObject:
    try:
        return callback()
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid Sudoku input: {exc}") from exc


def _run_single_strategy(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
    finder: SingleStrategyFinder,
) -> JsonObject:
    def run() -> JsonObject:
        candidates, validation_result = _validate_finder_input(
            board,
            solution,
            candidate_board,
        )
        if validation_result is not None:
            return validation_result

        assert candidates is not None
        placements = finder(candidates)
        return {"placements": _jsonify_cell_changes(placements)}

    return _run_with_input_errors(run)


def _run_removal_strategy(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
    finder: RemovalStrategyFinder,
) -> JsonObject:
    def run() -> JsonObject:
        candidates, validation_result = _validate_finder_input(
            board,
            solution,
            candidate_board,
        )
        if validation_result is not None:
            return validation_result

        assert candidates is not None
        removals, reasons = finder(candidates)
        return {
            "removals": _jsonify_cell_changes(removals),
            "reasons": _jsonify_positions(reasons),
        }

    return _run_with_input_errors(run)


def _validate_finder_input(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> tuple[ValidatedCandidateBoard | None, JsonObject | None]:
    """Validate board first, then candidates, before a strategy runs."""
    validated_board, deleted_cells = sudoku_validate_board_against_solution(
        _copy_board(board),
        _copy_board(solution),
    )
    if deleted_cells:
        return None, {
            "board": validated_board,
            "deleted_cells": _jsonify_cell_changes(deleted_cells),
        }

    (
        validated_candidates,
        deleted_candidates,
        missing_candidates,
    ) = sudoku_validate_candidates_against_board(
        validated_board,
        _copy_board(solution),
        _candidate_board_from_json(candidate_board),
    )
    if not deleted_candidates and not missing_candidates:
        return validated_candidates, None

    validation_result: JsonObject = {
        "candidate_board": _candidate_board_to_json(validated_candidates),
    }
    if deleted_candidates:
        validation_result["deleted_candidates"] = _jsonify_cell_changes(deleted_candidates)
    if missing_candidates:
        validation_result["missing_candidates"] = _jsonify_cell_changes(missing_candidates)
    return validated_candidates, validation_result


def _serialize_strategy_result(result: Any) -> JsonObject:
    if isinstance(result, tuple):
        removals, reasons = result
        return {
            "removals": _jsonify_cell_changes(removals),
            "reasons": _jsonify_positions(reasons),
        }

    return {"placements": _jsonify_cell_changes(result)}


@mcp.tool()
def validate_board_against_solution(
    board: JsonBoard,
    solution: JsonBoard,
) -> JsonObject:
    """Remove invalid values; reported row and column coordinates are 1-based."""

    def run() -> JsonObject:
        board_copy = _copy_board(board)
        solution_copy = _copy_board(solution)
        validated_board, deleted_cells = sudoku_validate_board_against_solution(
            board_copy,
            solution_copy,
        )
        return {
            "board": validated_board,
            "deleted_cells": _jsonify_cell_changes(deleted_cells),
        }

    return _run_with_input_errors(run)


@mcp.tool()
def validate_candidates_against_board(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Validate candidates; reported row and column coordinates are 1-based."""

    def run() -> JsonObject:
        board_copy = _copy_board(board)
        candidates = _candidate_board_from_json(candidate_board)
        (
            validated_candidates,
            deleted_candidates,
            missing_candidates,
        ) = sudoku_validate_candidates_against_board(
            board_copy,
            _copy_board(solution),
            candidates,
        )
        return {
            "candidate_board": _candidate_board_to_json(validated_candidates),
            "deleted_candidates": _jsonify_cell_changes(deleted_candidates),
            "missing_candidates": _jsonify_cell_changes(missing_candidates),
        }

    return _run_with_input_errors(run)


@mcp.tool()
def find_next_step(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject | None:
    """Return the next strategy; all reported row and column coordinates are 1-based."""

    def run() -> JsonObject | None:
        candidates, validation_result = _validate_finder_input(
            board,
            solution,
            candidate_board,
        )
        if validation_result is not None:
            return validation_result

        assert candidates is not None
        next_step = sudoku_find_next_step(candidates)

        if next_step is None:
            return None

        strategy, result = next_step
        return {
            "strategy": strategy,
            "result": _serialize_strategy_result(result),
        }

    return _run_with_input_errors(run)


@mcp.tool()
def find_single_candidates(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find cells with exactly one remaining candidate."""

    return _run_single_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_single_candidates,
    )


@mcp.tool()
def find_single_positions(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find candidates with only one possible position in a unit."""

    return _run_single_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_single_positions,
    )


@mcp.tool()
def find_candidate_lines(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the candidate lines strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_candidate_lines,
    )


@mcp.tool()
def find_double_pairs(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the double pairs strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_double_pairs,
    )


@mcp.tool()
def find_multiple_lines(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the multiple lines strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_multiple_lines,
    )


@mcp.tool()
def find_naked_pairs(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the naked pairs strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_naked_pairs,
    )


@mcp.tool()
def find_naked_triples(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the naked triples strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_naked_triples,
    )


@mcp.tool()
def find_naked_quads(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the naked quads strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_naked_quads,
    )


@mcp.tool()
def find_hidden_pairs(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the hidden pairs strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_hidden_pairs,
    )


@mcp.tool()
def find_hidden_triples(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the hidden triples strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_hidden_triples,
    )


@mcp.tool()
def find_hidden_quads(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the hidden quads strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_hidden_quads,
    )


@mcp.tool()
def find_x_wings(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the X-Wing strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_x_wings,
    )


@mcp.tool()
def find_swordfish(
    board: JsonBoard,
    solution: JsonBoard,
    candidate_board: JsonCandidateBoard,
) -> JsonObject:
    """Find removals using the swordfish strategy."""

    return _run_removal_strategy(
        board,
        solution,
        candidate_board,
        sudoku_find_swordfish,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
