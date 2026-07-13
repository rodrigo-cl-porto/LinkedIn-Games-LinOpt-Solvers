from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..gameboard import GameBoard


class Sudoku(GameBoard):
    """General Sudoku game."""
    
    def __init__(self, size: int, block_dims: tuple[int, int], filled_squares: dict[tuple[int, int]: int]) -> None:
        super().__init__((size, size)) # Always a square board.
        self.block_dims = block_dims
        self.filled_squares = filled_squares


    def __hash__(self):
        return hash((self.size, self.block_dims, self.filled_squares))


    @property
    def size(self) -> int:
        """The size of the Sudoku board (number of rows or columns)."""
        return self.board_dims[0]


    @property
    def block_dims(self) -> tuple[int, int]:
        """The dimensions of the grid blocks in the Sudoku board (rows, columns)."""
        return self._block_dims

    @block_dims.setter
    def block_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        
        if len(value) != 2:
            msg = f"Board dimensions must be a pair (m,n). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(not isinstance(dim, int) or isinstance(dim, bool) for dim in value):
            msg = f"Board dimensions must be integers. Got {value!r} instead."
            raise TypeError(msg)
        
        if any(dim < 1 for dim in value):
            msg = f"Board dimensions must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        p, q = value
        if p * q < 2:
            msg = f"The grid blocks is too small for the game! Got block dimensions of {value!r}."
            raise ValueError(msg)
        
        elif p * q != self.size:
            msg = f"The dimensions of grid blocks must match with the sudoku's size of {self.size}."
            raise ValueError(msg)

        if not isinstance(value, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, block dimensions should be a tuple."
                f"Got a {type(value).__name__} instead."
            ))
            value = tuple(value)
        
        self._block_dims = value
        self._stale = True


    @property
    def filled_squares(self) -> dict[tuple[int, int]: int]:
        """Returns the filled squares in the Sudoku board as a dictionary mapping (i,j) coordinates to their respective numbers."""
        return self._filled_squares
    
    @filled_squares.setter
    def filled_squares(self, values: dict[tuple[int, int]: int]) -> None:

        if len(values) > len(self):
            msg = (
                "The number of filled squares exceeds the amount of board squares! "
                f"Got {len(values)} filled squares, while the game board has {len(self)} squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of filled squares is too small for the game! "
                f"Got a total of {len(values)} filled squares."
            )
            raise ValueError(msg)

        if isinstance(values, (list, tuple)):
            print((
                "WARNING: The filled squares should be a dictionary mapping (i,j) coordinates to their respective numbers. "
                f"Got a {type(values).__name__} instead."
            ))
            self._filled_squares = {square: index for index, square in enumerate(values)}

        elif not isinstance(values, dict):
            msg = "The filled squares must be a dictionary."
            raise ValueError(msg)
        
        else:
            self._filled_squares = values

        nx.set_node_attributes(self.board, name="value", values=None)
        nx.set_node_attributes(self.board, name="value", values=self.filled_squares)
        self._stale = True


    def _construct_model(self) -> None:
        
        model = self.model
        
        # RANGE SETS
        n = self.size
        p, q = self.block_dims
        I = model.I # Rows
        J = model.J # Columns
        K = model.K = pyo.RangeSet(n) # Digits
        U = model.u = pyo.RangeSet(p) # Rows per block
        V = model.v = pyo.RangeSet(q) # Columns per block

        # COMPOSITE SETS
        B = model.B = pyo.Set( # Grid-blocks
            V, U,
            initialize= lambda model, v, u: 
            [(i, j) for i in range(p*(v-1)+1, p*v+1) for j in range(q*(u-1)+1, q*u+1)]
        )
        F = model.F = pyo.Set( # Filled values
            initialize=((i, j, k) for (i,j), k in self.filled_squares.items()),
            dimen=3
        )
        
        # DECISION VARIABLES
        x = model.x = pyo.Var(I, J, K, within=pyo.Binary, initialize=0)
        
        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0) # feasible problem
        
        # CONSTRAINTS
        model.unique_digits_per_row_constraints = pyo.Constraint(
            J, K,
            rule=lambda model, j, k: sum(x[i,j,k] for i in I) == 1
        )

        model.unique_digits_per_column_constraints = pyo.Constraint(
            I, K,
            rule=lambda model, i, k: sum(x[i,j,k] for j in J) == 1
        )

        model.unique_digits_per_block_constraints = pyo.Constraint(
            V, U, K,
            rule=lambda model, v, u, k: sum(x[i,j,k] for (i, j) in B[v,u]) == 1
        )

        model.single_digit_per_square_constraints = pyo.Constraint(
            I, J,
            rule=lambda model, i, j: sum(x[i,j,k] for k in K) == 1
        )

        model.alreadey_filled_squares_constraints = pyo.Constraint(
            F,
            rule=lambda model, i, j, k: x[i,j,k] == 1
        )


    def _set_solution(self, verbose:bool=False):

        # Saving the solution in the Sudoku board.
        nx.set_node_attributes(
            self.board,
            name="value",
            values= {
                (i-1, j-1): k
                for i in self.model.I 
                for j in self.model.J
                for k in self.model.K
                if pyo.value(self.model.x[i, j, k]) == 1
            }
        )
        
        if verbose:
            print("These are the digits for each square:")
            pprint(self.board_squares)


    def _show(self) -> None:

        plt.figure(figsize=(3, 3))

        nx.draw(
            self.board,
            pos= {(i, j): (j, -i) for (i, j) in self.board.nodes()},
            with_labels= True,
            labels= {
                node: data.get("value") if data.get("value") is not None else ""
                for node, data in self.board.nodes(data=True)
            },
            font_color="white",
            node_size= 1100,
            node_shape="s",
            node_color= "#1B1F22",
            width= 0,
            edgecolors="#999999",
            linewidths= .5,
        )

        plt.show()


class MiniSudoku(Sudoku):
    """A 6x6 Sudoku game with 2x3 grid blocks."""

    def __init__(self, filled_squares: dict[tuple[int, int]: int]) -> None:
        super().__init__(size=6, block_dims=(2,3), filled_squares=filled_squares)


class ClassicSudoku(Sudoku):
    """A 9x9 Sudoku game with 3x3 grid blocks."""

    def __init__(self, filled_squares: dict[tuple[int, int]: int]) -> None:
        super().__init__(size=9, block_dims=(3,3), filled_squares=filled_squares)
