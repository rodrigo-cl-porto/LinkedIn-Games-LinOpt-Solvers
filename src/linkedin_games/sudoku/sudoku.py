from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._game_board import GameBoard
from ._model import SudokuModel


class Sudoku(GameBoard):
    """A general Sudoku game."""
    def __init__(self, size: int, block_dims: tuple[int, int], filled_squares: dict[tuple[int, int], int]) -> None:
        super().__init__((size, size)) # Always a square board.
        self.__set_block_dims(block_dims)
        self.__set_filled_squares(filled_squares)
        self._model = SudokuModel(self.board_dims, self.block_dims, self.filled_squares)


    def __hash__(self) -> int:
        return hash((self.size, self.block_dims, self.filled_squares))


    @property
    def size(self) -> int:
        """The size of the Sudoku board (number of rows or columns)."""
        return self.board_dims[0]


    @property
    def block_dims(self) -> tuple[int, int]:
        """The dimensions of the grid blocks in the Sudoku board (rows, columns)."""
        return self.__block_dims

    def __set_block_dims(self, value:tuple[int, int] = (2, 2)) -> None:
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
            msg = (
                "The grid blocks is too small for the game."
                f" Got block dimensions of {value!r}."
            )
            raise ValueError(msg)
        
        if p * q != self.size:
            msg = (
                "The dimensions of grid blocks must match"
                f"with the sudoku's size of {self.size}."
            )
            raise ValueError(msg)
        
        self.__block_dims = tuple(value)


    @property
    def filled_squares(self) -> dict[tuple[int, int]: int]:
        """
        Return the filled squares in the Sudoku board as a dictionary mapping (i,j)
        coordinates to their respective numbers.
        """
        return self.__filled_squares
    
    def __set_filled_squares(self, values: dict[tuple[int, int]: int]) -> None:
        if len(values) > len(self):
            msg = (
                "The number of filled squares exceeds the amount of board squares."
                f" Got {len(values)} squares, but the board has {len(self)} squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of filled squares is too small for the game."
                f" Got a total of {len(values)} filled squares."
            )
            raise ValueError(msg)

        if isinstance(values, (list, tuple)):
            self.__filled_squares = {
                square: index for index, square in enumerate(values)
            }
        elif not isinstance(values, dict):
            msg = "The filled squares must be a dictionary."
            raise TypeError(msg)
        else:
            self.__filled_squares = values

        nx.set_node_attributes(self.board, name="value", values=None)
        nx.set_node_attributes(self.board, name="value", values=self.filled_squares)


    @property
    def solution(self) -> dict[tuple[int, int]: int] | None:
        if not self.is_solved:
            return None
        return self.board_squares

    def _set_solution(self, verbose:bool=False) -> None:
        nx.set_node_attributes(
            self.board,
            name="value",
            values= {
                (i-1, j-1): k
                for i in self.model.I
                for j in self.model.J
                for k in self.model.K
                if int(pyo.value(self.model.x[i, j, k])) == 1
            }
        )
        if verbose:
            print("These are the digits for each square:")
            pprint(self.solution)


    def show(self) -> None:
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
