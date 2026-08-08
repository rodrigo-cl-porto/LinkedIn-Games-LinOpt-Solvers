from .general_sudoku import GeneralSudoku


class Sudoku(GeneralSudoku):
    """
    The classic Sudoku game.
    
    A 9x9 Sudoku board with 3x3 grid blocks.

    Objective:
        Fill all the empty spaces in the game grid with digits from 1 to 9.

    Rule:
        Each row, column, and 3x3 block must be filled with a digit from 1 to 9,
        without repetition in each row, column, or block.
    """

    def __init__(self, filled_squares: dict[tuple[int, int], int]) -> None:
        """
        Args:
            filled_squares: Starting filled squares as a dictionary of `(row, column): digit` items.
        """
        super().__init__(size=9, block_dims=(3,3), filled_squares=filled_squares)
