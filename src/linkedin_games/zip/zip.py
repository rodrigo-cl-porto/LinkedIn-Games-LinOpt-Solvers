from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._color_generator_mixin import ColorGeneratorMixin
from ..core._game_board import GameBoard
from ._model import ZipModel


class Zip(ColorGeneratorMixin, GameBoard):
    """
    The [LinkedIn Zip](https://www.linkedin.com/games/zip/) game.
    
    A game board with some numbered squares and walls (walls are optional).
    
    Objective:
        To trace a single path that runs through all the board squares.

    Rule:
        The path must move through numbered squares in ascending order,
        starting from square number 1 to the one with the highest number.
    """
    def __init__(self,
            size:int,
            numbered_squares: list[tuple[int, int]],
            walls: list[tuple[tuple[int, int], tuple[int, int]]] | None = None) -> None:
        """
        Args:
            size: The side length of the game.
            numbered_squares: Squares with a assigned number as a dictionary of `(row, column): number` items.
            walls: Pairs of squares separated by a walls as a set of `((row1, column1), (row2, column2))`.
        
        Raises:
            TypeError: If the types of the arguments don't match their required types.
            ValueError: If the quantity of numbered squares exceeds the total number of squares on the board,
                or if the number of walls exceeds the total number of edges on the board,
                or if any pair of squares in walls are not adjacent.
        """
        super().__init__(board_dims=(size,size))
        self.__set_numbered_squares(numbered_squares)
        self.__set_walls(walls)
        self._model = ZipModel(self.board_dims, self.numbered_squares, self.walls)


    def __hash__(self) -> int:
        return hash((self._board_dims, self.__numbered_squares, self.__walls))


    @property
    def size(self) -> int:
        """The side length of the game.

        Returns:
            The number of rows (or columns) on game's board.
        """
        return self.board_dims[0]


    @property
    def number_of_edges(self) -> int:
        """
        The number of edges on board.
        
        Returns:
            The total number of edges on game board.
        """
        return self.board.number_of_edges() / 2


    @property
    def numbered_squares(self) -> list[tuple[int, int]]:
        """
        The squares with a assigned number.

        Returns:
            The numbered squares as a dictionary of `(row, column): number` items.
        """
        return self.__numbered_squares
    
    def __set_numbered_squares(self, values:list[tuple[int, int]]) -> None:

        if len(values) > len(self):
            msg = (
                "The quantity of numbered squares exceeds the amount of board squares."
                f" Got {len(values)} squares, while the board has {len(self)} squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of numbered squares is too small for the game."
                f" Got a total of {len(values)} numbered squares."
            )
            raise ValueError(msg)

        if not isinstance(values, list):
            msg = f"The numbered squares must be a list of tuples. Got a {type(values).__name__} instead."
            raise TypeError(msg)

        self.__numbered_squares = values
        nx.set_node_attributes(
            self.board,
            name="value",
            values= {square: index for index, square in enumerate(values)}
        )


    @property
    def walls(self) -> list[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        The pairs of squares separated by a wall.
        
        Returns:
            All the board edges blocked by a wall as a tuple of `((row1, column1), (row2, column2))`.
        """
        return self.__walls
    
    def __set_walls(self, values: set|tuple|list[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
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

        if not isinstance(values, (list, tuple, set)):
            msg = f"Walls must be a tuple, list or set of squares. Got a {type(values).__name__} instead."
            raise TypeError(msg)

        invalid_items = [pair for pair in values if self._manhattan_distance(*pair) != 1]
        if invalid_items:
            msg = f"Squares in a pair must be consecutive ones. Invalid pairs: {invalid_items!r}."
            raise ValueError(msg)

        self.__walls = list(set(values))


    @property
    def path(self) -> list[tuple[int, int]] | None:
        """
        The solving path of Zip game.
        
        The path that visits all the board squares, starting from 1-numbered squared to the highest-numbered square.

        Returns:
            The solving path as a list of squares as `(row, column)`.
        """
        if not self.is_solved:
            return None
        return self.__path

    def _set_solution(self, verbose:bool=False) -> None:
        nx.set_node_attributes(
            self.board,
            name="value",
            values={(i-1, j-1): round(pyo.value(self.model.u[i,j])) for i, j in self.model.S}
        )
        nx.set_edge_attributes(
            self.board,
            name="value",
            values={
                ((i-1, j-1), (r-1, s-1)): round(pyo.value(self.model.x[i,j,r,s]))
                for i, j, r, s in self.model.E
            }
        )
        path = nx.get_node_attributes(self.board, "value")
        path = sorted(path.keys(), key=path.get)
        self.__path = [(i+1, j+1) for (i, j) in path]
        if verbose:
            print("This is the path that solves the games:")
            pprint(self.path)


    def show(self) -> None:
        """Show Zip's board."""
        
        width = height = self.size * 0.7
        plt.figure(figsize=(width, height))
        path_color = super()._generate_hex_code()
        labels = {self.model.N.at(k): k for k in self.model.K}
        labels = {(i-1, j-1): k for (i,j), k in labels.items()}
        pos={(i,j): (j,-i) for i, j in self.board.nodes()}

        if self.walls is not None:
            walls = nx.draw_networkx_edges(
                self.board,
                pos=pos,
                edgelist=[((i-1, j-1), (r-1, s-1)) for (i,j),(r,s) in self.walls],
                edge_color="#000000",
                hide_ticks=True,
                arrows=False,
                width=30
            )
            walls.set_zorder(0)

        board_squares = nx.draw_networkx_nodes(
            self.board,
            pos= pos,
            node_shape="s",
            node_size= 1100,
            node_color= "#FFFFFF",
            linewidths= 2,
        )
        board_squares.set_zorder(1)

        nx.draw( # Drawing the path
            self.board,
            pos= pos,
            with_labels= True,
            labels=labels,
            arrows=False,
            node_shape="o" if self.is_solved else "s",
            node_size= 800,
            node_color= [
                "white" if (i+1,j+1) in self.numbered_squares else path_color
                for (i,j) in self.board.nodes()
            ],
            edge_color= path_color,
            edgecolors= path_color,
            linewidths= 1,
            width= 30,
            edgelist= [
                ((i-1, j-1), (r-1, s-1)) for i,j,r,s in self.model.E
                if round(pyo.value(self.model.x[i,j,r,s])) == 1
            ]
        )

        plt.show()
