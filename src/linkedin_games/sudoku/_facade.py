from abc import ABC, abstractmethod

from .._shared.domain.game_facade import GameFacade
from ._game_grid import SudokuGrid


class SudokuFacade(GameFacade, ABC):
    _game: SudokuGrid

    def __init__(self, size: int, filled_squares: dict[tuple[int, int], int]) -> None:
        super().__init__(size, filled_squares)

    @abstractmethod
    def _set_game(self, filled_squares: dict[tuple[int, int], int]) -> None:
        ...

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
