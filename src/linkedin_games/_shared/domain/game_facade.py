from typing import Any

from ..optimization.solve_game import SolveGame
from ..visualization.show_game import ShowGame
from .game_grid import GameGrid


class GameFacade:

    def __init__(self) -> None:
        self._game: GameGrid


    @property
    def size(self) -> int:
        """The side length of the game.

        Returns:
            The number of rows (or columns) on game's grid.
        """
        return self._game.grid_dims[0]


    @size.setter
    def size(self, value: int) -> None:
        if value < 1:
            msg = f"Game's size must be a positive integer. Got {value} instead."
            raise ValueError(msg)
        self._size = value

    @property
    def grid_dims(self) -> tuple[int, int]:
        """
        The grid dimensions.
        
        Returns:
            Dimensions of the grid as a `(rows, columns)` tuple.
        """
        return self._game.grid_dims


    @property
    def grid_squares(self) -> dict[tuple[int, int], Any]:
        """
        All the grid squares and their respective assigned values (if any).
        
        Returns:
            Grid squares as a dictionary of `(row, column): value` items.
        """
        return self._game.grid_squares


    def solve(self, solver: str = "highs", verbose: bool = False) -> None:
        self._game = SolveGame(self._game).execute(solver=solver, verbose=verbose)


    def display(self) -> None:
        ShowGame(self._game).execute()
