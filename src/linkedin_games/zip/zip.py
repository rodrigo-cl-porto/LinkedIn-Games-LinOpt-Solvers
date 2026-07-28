from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._game_board import GameBoard
from ._model import ZipModel


class Zip(GameBoard):
    """
    LikedIn Zip game

    Args:
        board_dims (tuple[int, int]): Dimensions of the Zip board as a tuple (rows, columns).
        numbered_squares (dict[tuple[int, int], int]): A dictionary where the keys are
            tuples representing the coordinates of the numbered squares on the board,
            and the values are the corresponding numbers assigned to those squares.
        walls (tuple[tuple[int, int]]|None): Walls on the Zip board.
            Each pair consists of coordinates of adjacent squares
            that are separated by a wall. If no walls are present, this
            argument can be set to None.
    
    Raises:
        ValueError: If the number of numbered squares exceeds the total number of squares
            on the board, or if the number of walls exceeds the total number of edges on
            the board, or if any pair of squares in walls are not adjacent.
    """
    def __init__(self,
            board_dims: tuple[int, int],
            numbered_squares: dict[tuple[int, int]: int],
            walls: tuple[tuple[int, int]]|None = None) -> None:
        super().__init__(board_dims)
        self.__set_numbered_squares(numbered_squares)
        self.__set_walls(walls)
        self._model = ZipModel(self.board_dims, self.numbered_squares, self.walls)


    def __hash__(self) -> int:
        return hash((self._board_dims, self.__numbered_squares, self.__walls))


    def number_of_edges(self) -> int:
        """Total number of edges on game board."""
        return len(self.board.number_of_edges()) / 2


    @property
    def numbered_squares(self) -> dict[tuple[int, int]: int]:
        """
        Return the numbered squares on the Zip board,
        where the keys are (row, column) coordinates
        and the values are the corresponding numbers assigned to those squares.
        """
        return self.__numbered_squares
    
    def __set_numbered_squares(self, values:dict[tuple[int, int]: int]) -> None:
        if len(values) > len(self):
            msg = (
                "The number of numbered squares exceeds the amount of board squares."
                f" Got {len(values)} squares, while the board has {len(self)} squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of numbered squares is too small for the game."
                f" Got a total of {len(values)} numbered squares."
            )
            raise ValueError(msg)

        if isinstance(values, (list, tuple)):
            self.__numbered_squares = {square: index for index, square in enumerate(values)}
        elif not isinstance(values, dict):
            msg = "The numbered squares must be a dictionary."
            raise TypeError(msg)
        else:
            self.__numbered_squares = values

        nx.set_node_attributes(self.board, name="value", values=None)
        nx.set_node_attributes(self.board, name="value", values=self.numbered_squares)


    @property
    def walls(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Returns a tuple of walls (pairs of squares)"""
        return self.__walls
    
    def __set_walls(self, values:tuple[tuple[int, int], tuple[int, int]] | None) -> None:
        if values is None:
            self.__walls = None
            return

        if len(values) > self.number_of_edges:
            msg = (
                "The number of walls exceeds the amount of board edges."
                f" Got {len(values)} numbered squares,"
                f" but the board has {self.number_of_edges} squares."
            )
            raise ValueError(msg)

        if isinstance(values, list):
            self.__walls = tuple(values)
        elif not isinstance(values, tuple):
            msg = "Walls must be a tuple of squares."
            raise TypeError(msg)
        else:
            self.__walls = values

        invalid_items = [pair for pair in values if super()._manhattan_distance(*pair) != 1]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)


    @property
    def path(self) -> list[tuple[int, int]] | None:
        """Return the path that solves the Zip game."""
        return self.solution

    @property
    def solution(self) -> list[tuple[int, int]] | None:
        """Return the path that solves the Zip game."""
        if not self.is_solved:
            return None
        return self.__solution

    def _set_solution(self, verbose:bool=False) -> None:
        nx.set_node_attributes(
            self.board,
            name="value",
            values={(i-1, j-1): round(pyo.value(self.model.u[i,j])) for i, j in self.model.S}
        )
        nx.set_edge_attributes(
            self.board,
            name="value",
            values={((i-1, j-1), (r-1, s-1)): round(pyo.value(self.model.x[i,j,r,s])) for i, j, r, s in self.model.E}
        )
        path = nx.get_node_attributes(self.board, "value")
        path = sorted(path.keys(), key=path.get)
        self.__solution = [(i+1, j+1) for (i, j) in path]
        if verbose:
            print("This is the path that solves the games:")
            pprint(self.solution)


    def show(self) -> None:
        plt.figure(figsize=(3.4, 3.4))
        path_color:str="#EE5F12"
        nx.draw(
            self.board,
            pos= {(i,j): (j,-i) for i, j in self.board.nodes()},
            with_labels= True,
            labels= {(i-1, j-1): self.model.k[i,j] for (i, j) in self.model.K},
            arrows=False,
            node_shape="o", # round nodes
            node_size= 1000,
            node_color= [
                "white" if (i+1,j+1) in self.numbered_squares else path_color
                for (i,j) in self.board.nodes()
            ],
            edge_color= path_color,
            edgecolors= path_color,
            linewidths= 3,
            width= 35,
            edgelist= [
                ((i-1, j-1), (r-1, s-1)) for i,j,r,s in self.model.E
                if round(pyo.value(self.model.x[i,j,r,s])) == 1
            ]
        )
        plt.show()
