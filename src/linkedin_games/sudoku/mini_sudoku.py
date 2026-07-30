from .sudoku import Sudoku


class MiniSudoku(Sudoku):
    """The 6x6 LinkedIn Mini Sudoku game, with 2x3 grid blocks."""
    
    def __init__(self, filled_squares: dict[tuple[int, int], int]) -> None:
        """
        Args:
            filled_squares: Starting filled squares as a dictionary of `(row, column): digit` values.
        """
        super().__init__(size=6, block_dims=(2,3), filled_squares=filled_squares)
