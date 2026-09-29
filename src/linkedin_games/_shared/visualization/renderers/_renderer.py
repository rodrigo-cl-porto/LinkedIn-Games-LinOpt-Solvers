from abc import ABC, abstractmethod

import networkx as nx

from ...domain.game_grid import GameGrid


class GameRenderer[G: GameGrid](ABC):

    _SCALE_FACTOR = .5

    def __init__(self, game: G) -> None:
        self._game = game
        m, n = game.grid_dims
        self._height = m * self._SCALE_FACTOR
        self._width = n * self._SCALE_FACTOR
        self._set_grid()


    @abstractmethod
    def _set_grid(self) -> None:
        self._grid = nx.grid_2d_graph(*self._game.grid_dims).to_directed()
        nx.set_node_attributes(self._grid, name="value",
            values={(i-1, j-1): k for (i, j), k in self._game.grid_squares.items()}
        )


    @abstractmethod
    def show(self) -> None:
        ...
