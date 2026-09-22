from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..._core._game_grid import GameGrid
from ._model import SudokuModel


class BaseSudoku(GameGrid):
    """
    A general Sudoku game.

    A `n`x`n` Sudoku grid with `p`x`q` grid block (where is expected that `p * q = n`).
    
    Objective:
        Fill all the empty spaces in the game grid with digits from 1 to `n`.
    
    Rules:
        Each row, column, and block must be filled with a digit from 1 to `n`,
        without repetition in each row, column, or `p`x`q` block.
    """
    def __init__(self, size: int, block_dims: tuple[int, int], filled_squares: dict[tuple[int, int], int]) -> None:
        """
        Args:
            size: The Sudoku's number of rows (or columns).
            block_dims: Grid dimensions as a `(rows, columns)` tuple.
            filled_squares: The starting filled squares as a dictionary of `(row, column): digit` items.

        Raises:
            TypeError: if the input types are not respected.
            ValueError: if `p * q = n` is not respected
                or if the quantity of `filled_squares` is smaller than 2
                or greater than the number of grid squares.
        """
        super().__init__((size, size))
        self.__set_block_dims(block_dims)
        self.__set_filled_squares(filled_squares)
        self._model = SudokuModel(self.grid_dims, self.block_dims, self.filled_squares)


    def __hash__(self) -> int:
        return hash((self._grid_dims, self.__block_dims, self.__filled_squares))


    def __eq__(self, other: object) -> bool:

        if not isinstance(other, BaseSudoku):
            return False
        
        return (
            self.size == other.size
            and self.block_dims == other.block_dims
            and self.filled_squares == other.filled_squares
        )


    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


    @property
    def size(self) -> int:
        """
        The size of Sudoku game.

        Returns:
            The number of rows (or columns) on the grid.
        """
        return self.grid_dims[0]


    @property
    def block_dims(self) -> tuple[int, int]:
        """
        The dimensions of the grid blocks in the Sudoku grid
        
        Returns:
            The block dimensions as `(rows, columns)` tuple.
        """
        return self.__block_dims

    def __set_block_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        
        if len(value) != 2:
            msg = f"Grid dimensions must be a pair (m,n). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(not isinstance(dim, int) or isinstance(dim, bool) for dim in value):
            msg = f"Grid dimensions must be integers. Got {value!r} instead."
            raise TypeError(msg)
        
        if any(dim < 1 for dim in value):
            msg = f"Grid dimensions must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        p, q = value
        if p * q < 2:
            msg = f"The grid blocks is too small for the game. Got block dimensions of {value!r}."
            raise ValueError(msg)
        
        if p * q != self.size:
            msg = f"The dimensions of grid blocks must match with the sudoku's size of {self.size}."
            raise ValueError(msg)
        
        self.__block_dims = tuple(value)


    @property
    def filled_squares(self) -> dict[tuple[int, int], int]:
        """The starting filled squares in the Sudoku game.
        
        Returns:
            The starting filled squares as a dictionary of `(row, column): digit` items.
        """
        return self.__filled_squares
    
    def __set_filled_squares(self, values: dict[tuple[int, int], int]) -> None:

        if not isinstance(values, dict):
            msg = f"The filled squares must be a dictionary. Got a {type(values).__name__} instead."
            raise TypeError(msg)

        invalid_items = {
            square: digit for square, digit in values.items()
            if not isinstance(square, tuple) or not isinstance(digit, int)
        }
        if invalid_items:
            msg = (
                "filled_squares must be a dictionary of `(row, column): digit` items."
                f" Invalid items: {invalid_items}"
            )
            raise TypeError(msg)

        invalid_items = {square: digit for square, digit in values.items() if digit < 0 or digit > self.size}
        if invalid_items:
            msg = f"Digits must be positive and not greater than Sudoku's size. Invalid items: {invalid_items}"
            raise ValueError(msg)

        if len(values) > len(self):
            msg = (
                "The number of filled squares exceeds the amount of grid squares."
                f" Got {len(values)} squares, but the grid has {len(self)} squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of filled squares is too small for the game."
                f" Got a total of {len(values)} filled squares."
            )
            raise ValueError(msg)

        self.__filled_squares = values
        nx.set_node_attributes(self.grid, name="value", values=self.filled_squares)


    def _set_solution(self, verbose:bool=False) -> None:

        S = self.model.S
        K = self.model.K
        x = self.model.x
        nx.set_node_attributes(
            self.grid,
            name="value",
            values= {(i-1, j-1): k for (i, j) in S for k in K if round(pyo.value(x[i,j,k])) == 1}
        )
        if verbose:
            print("These are the digits for each square:")
            pprint(self.solution)


    def show(self) -> None:
        """Show the Sudoku's grid."""
        width = height = self.size * 0.5
        plt.figure(figsize=(width, height))
        nx.draw(
            self.grid,
            pos= {(i, j): (j, -i) for (i, j) in self.grid.nodes()},
            with_labels= True,
            arrows=False,
            labels= {
                node: data.get("value") if data.get("value") is not None else ""
                for node, data in self.grid.nodes(data=True)
            },
            font_color="white",
            node_size= 1100,
            node_shape="s",
            node_color= "#1B1F22",
            width= 0,
            edgecolors="#999999",
            linewidths= 1,
        )
        plt.show()
