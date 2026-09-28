from abc import ABC, abstractmethod

from ..optimization.solve_game import SolveGame
from ..visualization.show_game import ShowGame
from .games.game_grid import GameGrid


class GameFacade(ABC):

    def __init__(self) -> None:
        self._game: GameGrid


    @abstractmethod
    def solve(self, solver: str = "highs", verbose: bool = False) -> None:
        self._game = SolveGame(self._game).execute(solver=solver, verbose=verbose)

    @abstractmethod
    def display(self) -> None:
        ShowGame(self._game).execute()
