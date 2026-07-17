from abc import ABC, abstractmethod
from pyomo.opt import SolverStatus, TerminationCondition
import networkx as nx
import pyomo.environ as pyo


class GameBoard(ABC): # Abstract Base Class

    def __init__(self, board_dims:tuple[int, int]) -> None:
        self.board_dims = board_dims
        GameBoard._build_board(self)
        self._model: pyo.ConcreteModel | None = None
        self._stale: bool = True


    def __hash__(self) -> int:
        return hash(self._board_dims)


    def __len__(self) -> int:
        m, n = self._board_dims
        return m * n


    def __abs__(self) -> int:
        return len(self)


    @staticmethod
    def _manhattan_distance(square1:tuple[int, int], square2:tuple[int, int]) -> int:
        """Calculates the Manhattan distance between two squares."""
        x1, y1 = square1
        x2, y2 = square2
        return abs(x1 - x2) + abs(y1 - y2)


    @property
    def board_dims(self) -> tuple[int, int]:
        """A tuple of two integers representing the board dimensions (m,n)."""
        return self._board_dims

    @board_dims.setter
    def board_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        
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
            msg = f"The board is too small for the game! Got board dimensions of {value!r}."
            raise ValueError(msg)

        if not isinstance(value, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, board dimensions should be a tuple."
                f"Got a {type(value).__name__} instead."
            ))
            value = tuple(value)
        
        self._board_dims = value
        self._stale = True


    @property
    def board(self) -> nx.DiGraph:
        """A NetworkX DiGraph (directed graph) representing the game board."""
        return self._board

    def _build_board(self) -> None:
        board = nx.grid_2d_graph(*self._board_dims).to_directed()
        nx.set_node_attributes(board, name="value", values=None)
        nx.set_edge_attributes(board, name="value", values=None)
        self._board = board
        self._stale = True


    @property
    def board_squares(self) -> dict[tuple[int, int]: int]:
        """A dictionary of the board squares and their values."""
        return {(i+1, j+1): data["value"] for (i, j), data in self.board.nodes(data=True)}
    
    @property
    def board_edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]]: int]:
        """A dictionary of the board edges and their values."""
        edges = nx.get_edge_attributes(self.board, "value").items()
        return {((i+1, j+1), (r+1, s+1)): value for ((i, j), (r, s)), value in edges}


    @property
    def model(self) -> pyo.ConcreteModel | None:
        """A Pyomo ConcreteModel representing the Linear Optimization Problem for the game."""
        return self._model


    @property
    def _stale(self) -> bool:
        """A boolean indicating whether the model is stale and needs to be rebuilt."""
        return self.__stale
    
    @_stale.setter
    def _stale(self, value:bool) -> None:
        self.__stale = value

        if value:
            self.__is_solved = False
    
    
    @property
    def is_solved(self) -> bool:
        """A boolean indicating whether the game has been solved."""
        return self.__is_solved


    def _build_model(self) -> None:
        """Builds the Pyomo model for the game board."""
        
        model = pyo.ConcreteModel()

        # BOARD DIMENSIONS
        m, n = self._board_dims
        model.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        model.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = model.I = pyo.RangeSet(n) # Rows
        J = model.J = pyo.RangeSet(m) # Columns

        # COMPOSITE SETS
        model.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        
        # Attach model
        self._model = model
        self._construct_model()
        self._stale = False

    @abstractmethod
    def _construct_model(self) -> None:
        """Constructs the Pyomo model for the game board."""
        pass
    
    
    def solve(self, solver:str="gurobi", verbose:bool=False) -> pyo.ConcreteModel:
        """Solves the game board using the specified solver."""
        
        if self._stale or self.model is None:
            self._build_model()

        result = pyo.SolverFactory(solver).solve(self.model)

        self.__is_solved = (
            result.Solver.status == SolverStatus.ok # Checks if solver is finished with normal termination.
            and (
                result.Solver.termination_condition == TerminationCondition.optimal # Checks if solver is finished with an optimal solution...
                or result.Solver.termination_condition == TerminationCondition.feasible # ... or with a feasible one.
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
        """Sets the solution of the game board."""
        pass


    def show(self) -> None:
        """Displays the game board."""

        if self._stale or self._model is None:
            self._build_model()

        self._show()

    @abstractmethod
    def _show(self) -> None:
        """Displays the game board."""
        pass
