from abc import ABC, abstractmethod

import networkx as nx
import pyomo.environ as pyo


class GameGrid(ABC):
    """An Abstract Base Class for any LinkedIn game grid."""

    def __init__(self, grid_dims:tuple[int, int]) -> None:
        """
        Args:
            `grid_dims`: Grid dimensions as a `(rows, columns)` tuple.
        
        Raises:
            `TypeError`: If `grid_dims` is not a tuple of two integers.
            `ValueError`: If `grid_dims` is not a tuple of two positive integers
                or if the grid's area is smaller than 2 squares.
        """
        self._set_grid_dims(grid_dims)
        self._set_grid()
        self._model: pyo.ConcreteModel
        self.__is_solved:bool = False


    def __hash__(self) -> int:
        return hash(self._grid_dims)


    def __len__(self) -> int:
        m, n = self._grid_dims
        return m * n


    def __abs__(self) -> int:
        return len(self)


    @property
    def area(self) -> int:
        """
        The game grid's area

        Returns:
            The total number of squares on the grid.
        """
        return len(self)


    @property
    def grid_dims(self) -> tuple[int, int]:
        """
        The grid dimensions.
        
        Returns:
            Dimensions of the grid as a `(rows, columns)` tuple.
        """
        return self._grid_dims


    def _set_grid_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        if len(value) != 2:
            msg = f"Grid dimensions must be a pair (m,n). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(not isinstance(dim, int) or isinstance(dim, bool) for dim in value):
            msg = f"Grid dimensions must be integers. Got {value!r} instead."
            raise TypeError(msg)
        
        if any(dim < 1 for dim in value):
            msg = f"Grid dimensions must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        m, n = value
        if m * n < 2:
            msg = f"The grid is too small for the game. Got grid dimensions of {value!r}."
            raise ValueError(msg)
        
        self._grid_dims = tuple(value)


    @property
    def grid(self) -> nx.DiGraph:
        """
        The game's grid.
        
        The nodes of the graph represent the squares, and its edges represent the possible paths between squares.

        Returns:
            A directed graph representing the game's grid.
        """
        return self._grid


    def _set_grid(self) -> None:
        grid = nx.grid_2d_graph(*self._grid_dims).to_directed()
        nx.set_node_attributes(grid, name="value", values=None)
        nx.set_edge_attributes(grid, name="value", values=None)
        self._grid = grid


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


    @property
    def model(self) -> pyo.ConcreteModel:
        """
        The game's mathematical model.
        
        Returns:
            The Linear Optimization model of the game's problem.
        """
        return self._model

    
    @property
    def is_solved(self) -> bool:
        """
        Check if the game has been solved.
        
        Returns:
            `True` if the game has been solved. `False` otherwise.
        """
        return self.__is_solved


    @abstractmethod
    def _set_solution(self, verbose:bool) -> None:
        """Set the solution of the game grid."""
        ...

    @abstractmethod
    def show(self) -> None:
        """Display the game grid as a graph chart."""
        ...
