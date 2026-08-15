from abc import ABC, abstractmethod

import networkx as nx
import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition


class GameBoard(ABC):
    """An Abstract Base Class for any LinkedIn game board."""

    def __init__(self, board_dims:tuple[int, int]) -> None:
        """
        Args:
            `board_dims`: Board dimensions as a `(rows, columns)` tuple.
        
        Raises:
            `TypeError`: If `board_dims` is not a tuple of two integers.
            `ValueError`: If `board_dims` is not a tuple of two positive integers
                or if the board's area is smaller than 2 squares.
        """
        self._set_board_dims(board_dims)
        self._set_board()
        self._model: pyo.ConcreteModel
        self.__is_solved:bool = False


    def __hash__(self) -> int:
        return hash(self._board_dims)


    def __len__(self) -> int:
        m, n = self._board_dims
        return m * n


    def __abs__(self) -> int:
        return len(self)


    @property
    def area(self) -> int:
        """
        The game board's area

        Returns:
            The total number of squares on the board.
        """
        return len(self)


    @property
    def board_dims(self) -> tuple[int, int]:
        """
        The board dimensions.
        
        Returns:
            Dimensions of the board as a `(rows, columns)` tuple.
        """
        return self._board_dims

    def _set_board_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        if len(value) != 2:
            msg = f"Board dimensions must be a pair (m,n). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(not isinstance(dim, int) or isinstance(dim, bool) for dim in value):
            msg = f"Board dimensions must be integers. Got {value!r} instead."
            raise TypeError(msg)
        
        if any(dim < 1 for dim in value):
            msg = f"Board dimensions must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        m, n = value
        if m * n < 2:
            msg = f"The board is too small for the game. Got board dimensions of {value!r}."
            raise ValueError(msg)
        
        self._board_dims = tuple(value)


    @property
    def board(self) -> nx.DiGraph:
        """
        The game's board.
        
        The nodes of the graph represent the squares, and its edges represent the possible paths between squares.

        Returns:
            A directed graph representing the game's board.
        """
        return self._board

    def _set_board(self) -> None:
        board = nx.grid_2d_graph(*self._board_dims).to_directed()
        nx.set_node_attributes(board, name="value", values=None)
        nx.set_edge_attributes(board, name="value", values=None)
        self._board = board


    @property
    def board_squares(self) -> dict[tuple[int, int], int] | dict[tuple[int, int], str]:
        """
        All the board squares and their respective assigned values (if any).
        
        Returns:
            Board squares as a dictionary of `(row, column): value` items.
        """
        return {(i+1, j+1): data["value"] for (i, j), data in self.board.nodes(data=True)}
    
    @property
    def board_edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        """
        All the board edges and their respective assigned values (if any).
        
        Returns:
            All edges as a dictionary of `((row1, column1), (row2, column2)): value` items.
        """
        edges = nx.get_edge_attributes(self.board, "value").items()
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
        """Check if the game has been solved.
        
        Returns:
            `True` if the game has been solved. `False` otherwise.
        """
        return self.__is_solved


    @property
    def solution(self) -> dict[tuple[int, int], int] | dict[tuple[int, int], str] | None:
        """
        The solved game board.
        
        Returns:
            A dictionary of squares as `(row, column): value` or `None` if game's not solved yet.
        """
        if not self.is_solved:
            return None
        return self.board_squares


    def solve(self, solver:str="highs", verbose:bool=False) -> None:
        """
        Solve the game board using the specified solver.
        
        Args:
            solver: The solver's name to be used to solve the game.
            verbose: If `True`, prints the solver output.
        """
        result = pyo.SolverFactory(solver).solve(self.model)
        self.__is_solved = (
            result.Solver.status == SolverStatus.ok # Checks if solver is finished with normal termination and if...
            and(
                result.Solver.termination_condition == TerminationCondition.optimal # ended with an optimal solution...
                or result.Solver.termination_condition == TerminationCondition.feasible # or with a feasible one.
            )
        )
        if self.__is_solved:
            print(f"{type(self).__name__} game solved successfully!")
            self._set_solution(verbose=verbose)
        else:
            print("No feasible solution was found!")
            if verbose:
                print(result.Solver)


    @abstractmethod
    def _set_solution(self, verbose:bool) -> None:
        """Set the solution of the game board."""
        ...

    @abstractmethod
    def show(self) -> None:
        """Display the game board as a graph chart."""
        ...
