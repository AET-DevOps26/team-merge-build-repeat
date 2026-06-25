from __future__ import annotations

from collections.abc import Callable
from typing import Literal, TypeAlias

from sudoku_lib.strategy.candidate_lines import (
    CandidateLineReason,
    CandidateLineRemoval,
    find_candidate_lines,
)
from sudoku_lib.strategy.double_pairs import (
    DoublePairReason,
    DoublePairRemoval,
    find_double_pairs,
)
from sudoku_lib.strategy.fish import (
    FishReason,
    FishRemoval,
    find_swordfish,
    find_x_wings,
)
from sudoku_lib.strategy.multiple_lines import (
    MultipleLineReason,
    MultipleLineRemoval,
    find_multiple_lines,
)
from sudoku_lib.strategy.single_candidate import SingleCandidate, find_single_candidates
from sudoku_lib.strategy.single_position import SinglePosition, find_single_positions
from sudoku_lib.strategy.subsets import (
    SubsetReason,
    SubsetRemoval,
    find_hidden_pairs,
    find_hidden_quads,
    find_hidden_triples,
    find_naked_pairs,
    find_naked_quads,
    find_naked_triples,
)
from sudoku_lib.validation import ValidatedCandidateBoard

StrategyType = Literal[
    "single_candidate",
    "single_position",
    "candidate_lines",
    "double_pairs",
    "multiple_lines",
    "naked_pairs",
    "naked_triples",
    "naked_quads",
    "hidden_pairs",
    "hidden_triples",
    "hidden_quads",
    "x_wings",
    "swordfish",
]
SingleStrategyResult: TypeAlias = list[SingleCandidate] | list[SinglePosition]
RemovalStrategyResult: TypeAlias = (
    tuple[list[CandidateLineRemoval], list[CandidateLineReason]]
    | tuple[list[DoublePairRemoval], list[DoublePairReason]]
    | tuple[list[MultipleLineRemoval], list[MultipleLineReason]]
    | tuple[list[SubsetRemoval], list[SubsetReason]]
    | tuple[list[FishRemoval], list[FishReason]]
)
StrategyResult: TypeAlias = SingleStrategyResult | RemovalStrategyResult
NextStep: TypeAlias = tuple[StrategyType, StrategyResult]
StrategyFinder: TypeAlias = Callable[[ValidatedCandidateBoard], StrategyResult]


STRATEGY_ORDER: tuple[tuple[StrategyType, StrategyFinder], ...] = (
    ("single_candidate", find_single_candidates),
    ("single_position", find_single_positions),
    ("candidate_lines", find_candidate_lines),
    ("double_pairs", find_double_pairs),
    ("multiple_lines", find_multiple_lines),
    ("naked_pairs", find_naked_pairs),
    ("naked_triples", find_naked_triples),
    ("naked_quads", find_naked_quads),
    ("hidden_pairs", find_hidden_pairs),
    ("hidden_triples", find_hidden_triples),
    ("hidden_quads", find_hidden_quads),
    ("x_wings", find_x_wings),
    ("swordfish", find_swordfish),
)


def find_next_step(candidate_board: ValidatedCandidateBoard) -> NextStep | None:
    """
    Return the first applicable strategy result from easy to hard.

    The returned tuple contains the strategy type and the original result of
    that strategy finder. Return None if no strategy can remove or place
    anything.
    """

    for strategy_type, strategy_finder in STRATEGY_ORDER:
        result = strategy_finder(candidate_board)

        if _has_strategy_result(result):
            return strategy_type, result

    return None


def _has_strategy_result(result: StrategyResult) -> bool:
    if isinstance(result, tuple):
        removals, _ = result
        return bool(removals)

    return bool(result)
