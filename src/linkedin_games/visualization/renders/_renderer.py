from abc import ABC, abstractmethod

import networkx as nx

from ...domain._game_grid import GameGrid


class GameRenderer[G: GameGrid](ABC):

    def __init__(self, game: G) -> None:
        m, n = game.grid_dims
        self._height, self._width = m * .5, n * .5
        self.__set_grid(game)


    def __set_grid(self, game: G) -> None:
        grid = nx.grid_2d_graph(*game.grid_dims).to_directed()
        nx.set_node_attributes(grid, name="value", values=None)
        nx.set_edge_attributes(grid, name="value", values=None)
        self._grid = grid


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
        return {(i+1, j+1): data["value"] for (i, j), data in self.grid.nodes(data=True)}


    @property
    def grid_edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        """
        All the grid edges and their respective assigned values (if any).
        
        Returns:
            All edges as a dictionary of `((row1, column1), (row2, column2)): value` items.
        """
        edges = nx.get_edge_attributes(self.grid, "value").items()
        return {((i+1, j+1), (r+1, s+1)): value for ((i, j), (r, s)), value in edges}


    @abstractmethod
    def render(self, game: G) -> None:
        ...
