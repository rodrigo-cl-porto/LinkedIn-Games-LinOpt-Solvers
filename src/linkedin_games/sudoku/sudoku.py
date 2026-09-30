from .._shared.domain.game_facade import GameFacade
from ._game_grid import SudokuGrid


class Sudoku(GameFacade):
    """The classic Sudoku game.
    
    A 9x9 Sudoku board with 3x3 grid blocks.

    Objective:
        Fill all the empty spaces in the game grid with digits from 1 to 9.

    Rule:
        Each row, column, and 3x3 block must be filled with a digit from 1 to 9,
        without repetition in each row, column, or block.
    """

    _game: SudokuGrid

    def __init__(self, filled_squares: dict[tuple[int, int], int]) -> None:
        """
        Args:
            filled_squares: Starting filled squares as a dictionary of `(row, column): digit` items.
        """
        self._game = SudokuGrid(dims=(9,9), block_dims=(3,3), filled_squares=filled_squares)

    @property
    def block_dims(self) -> tuple[int, int]:
        """
        The dimensions of the grid blocks in the Sudoku grid
        
        Returns:
            The block dimensions as `(rows, columns)` tuple.
        """
        return self._game.block_dims

    @property
    def filled_squares(self) -> dict[tuple[int, int], int]:
        """The starting filled squares in the Sudoku game.
        
        Returns:
            The starting filled squares as a dictionary of `(row, column): digit` items.
        """
        return self._game.filled_squares
