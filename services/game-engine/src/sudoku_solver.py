from sudoku import Sudoku
import random

_sysrand = random.SystemRandom()

def map_difficulty_to_level(difficulty: str) -> float:
    """Map difficulty string to numeric difficulty level (0.0 to 1.0)"""
    difficulty_map = {
        "easy": 0.4,
        "medium": 0.5,
        "hard": 0.6,
    }
    return difficulty_map.get(difficulty.lower(), 0.6)

def generate_sudoku(difficulty: str = "medium"):
    difficulty_level = map_difficulty_to_level(difficulty)
    s = Sudoku(seed=_sysrand.randint(0, 10**15)).difficulty(difficulty_level)
    i = 0
    while s.has_multiple_solutions():
        s = Sudoku(seed=_sysrand.randint(0, 10**15)).difficulty(difficulty_level)
        i += 1
        if i > 100:
            raise ValueError("Konnte kein eindeutiges Sudoku generieren.")
    return s.board

def get_solution(board):
    s = Sudoku(board=board)
    return s.solve().board
