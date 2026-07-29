from .sudoku import Sudoku


class ClassicSudoku(Sudoku):
    """A 9x9 Sudoku game with 3x3 grid blocks."""
    def __init__(self, filled_squares: dict[tuple[int, int], int]) -> None:
        super().__init__(size=9, block_dims=(3,3), filled_squares=filled_squares)
