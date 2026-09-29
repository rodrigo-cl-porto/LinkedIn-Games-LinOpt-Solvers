from .._shared.domain.game_facade import GameFacade
from ._game_grid import SudokuGrid


class Sudoku(GameFacade):
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
        super().__init__()
        self._game = SudokuGrid(grid_dims=(9,9), block_dims=(3,3), filled_squares=filled_squares)


class MiniSudoku(GameFacade):
    """
    The [LinkedIn Mini Sudoku](https://www.linkedin.com/games/mini-sudoku/) game.

    A 6x6 Sudoku board with 2x3 grid blocks.

    Objective:
        Fill all the empty spaces in the game grid with digits from 1 to 6.
    
    Rules:
        Each row, column, and 2x3 block must be filled with a digit from 1 to 6,
        without repetition in each row, column, or block.
    """

    def __init__(self, filled_squares: dict[tuple[int, int], int]) -> None:
        """
        Args:
            filled_squares: Starting filled squares as a dictionary of `(row, column): digit` items.
        """
        super().__init__()
        self._game = SudokuGrid(grid_dims=(6,6), block_dims=(2,3), filled_squares=filled_squares)
