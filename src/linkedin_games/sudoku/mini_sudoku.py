from typing import Self

from .sudoku import Sudoku


class MiniSudoku(Sudoku):
    """A 6x6 Sudoku game with 2x3 grid blocks."""
    def __init__(self, filled_squares: dict[tuple[int, int]: int]) -> Self:
        super().__init__(size=6, block_dims=(2,3), filled_squares=filled_squares)
