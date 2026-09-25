from abc import ABC, abstractmethod

import networkx as nx

from ...domain.games.game_grid import GameGrid


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
        nx.set_edge_attributes(self._grid, name="value", values=None)
        if self._game.solution:
            nx.set_node_attributes(
                self._grid,
                name="value",
                values={(i-1, j-1): k for (i, j), k in self._game.grid_squares.items()}
            )
        else:
            nx.set_node_attributes(self._grid, name="value", values=None)


    @property
    def height(self) -> float:
        return self._height


    @property
    def width(self) -> float:
        return self._width


    @property
    def grid(self) -> nx.DiGraph:
        """
        The game's grid.
        
        The nodes of the graph represent the squares, and its edges represent the possible paths between squares.

        Returns:
            A directed graph representing the game's grid.
        """
        return self._grid


    @property
    def grid_squares(self) -> dict[tuple[int, int], int] | dict[tuple[int, int], str]:
        """
        All the grid squares and their respective assigned values (if any).
        
        Returns:
            Grid squares as a dictionary of `(row, column): value` items.
        """
        return {(i+1, j+1): data["value"] for (i, j), data in self._grid.nodes(data=True)}


    @property
    def grid_edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        """
        All the grid edges and their respective assigned values (if any).
        
        Returns:
            All edges as a dictionary of `((row1, column1), (row2, column2)): value` items.
        """
        edges = nx.get_edge_attributes(self._grid, "value").items()
        return {((i+1, j+1), (r+1, s+1)): value for ((i, j), (r, s)), value in edges}


    @abstractmethod
    def show(self) -> None:
        ...
