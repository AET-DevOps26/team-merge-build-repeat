from sudoku import Sudoku
import random

def generate_sudoku():
    s = Sudoku(seed=random.randint(0, 10000)).difficulty(0.5)
    i = 0
    while s.has_multiple_solutions():
        s = Sudoku(seed=random.randint(0, 10000)).difficulty(0.5)
        i += 1
        if i > 100:
            raise ValueError("Konnte kein eindeutiges Sudoku generieren.")
    return s.board
