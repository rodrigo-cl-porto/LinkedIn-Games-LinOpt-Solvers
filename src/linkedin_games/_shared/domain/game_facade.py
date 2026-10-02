from abc import ABC, abstractmethod
from typing import Any, Self

from ..optimization.solve_game import SolveGame
from ..visualization.show_game import ShowGame
from .game_grid import GameGrid


class GameFacade(ABC):
    _game: GameGrid

    def __init__(self, size: int, *args: Any, **kwargs: Any) -> None:
        self._set_size(size)
        self._set_game(*args, **kwargs)

    @property
    def size(self) -> int:
        """The side length of the game.

        Returns:
            The number of rows (or columns) on game's grid.
        """
        return self._game.dims[0]

    def _set_size(self, value: int) -> None:
        if value < 1:
            msg = f"Game's size must be a positive integer. Got {value} instead."
            raise ValueError(msg)
        self._size = value

    @abstractmethod
    def _set_game(self, *args: Any, **kwargs: Any) -> None:
        ...

    @property
    def dims(self) -> tuple[int, int]:
        """The game grid dimensions.

        Returns:
            Dimensions of the game as a `(rows, columns)` tuple.
        """
        return (self._size, self._size)

    @property
    def squares(self) -> dict[tuple[int, int], Any]:
        """All the grid squares and their respective assigned values (if any).
        
        Returns:
            Grid squares as a dictionary of `(row, column): value` items.
        """
        return self._game.squares

    @property
    def solution(self) -> dict[tuple[int, int], Any]:
        """The game's solution.

        Returns:
            A dictionary of squares with a value as `(row, column): value` items.
        """
        return self._game.solution

    def solve(self, solver: str = "highs", verbose: bool = False) -> Self:
        """Solves the game.
        
        Args:
            solver: The solver to be used. Options are "highs" (default), "glpk", and "cbc".
            verbose: Whether to print the solver's output. Default is False.

        Returns:
            The solved game
        """
        if self._game.is_solved:
            msg = "The game is already solved."
            raise RuntimeError(msg)
        SolveGame(self._game).execute(solver=solver, verbose=verbose)
        return self

    def display(self) -> None:
        """Displays the game in a graphical window."""
        ShowGame(self._game).execute()
