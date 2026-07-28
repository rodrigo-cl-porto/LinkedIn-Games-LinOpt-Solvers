from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._game_board import GameBoard
from ._model import TangoModel


class Tango(GameBoard):
    """_summary_

    Attributes:
        GameBoard (_type_): _description_
    """

    def __init__(self,
            filled_squares:dict[tuple[int, int]: int] | None = None,
            matching_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None = None,
            opposite_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None = None,
            ) -> None:
        super().__init__(board_dims=(6,6)) # It's assumed that Tango board dimensions will always be a 6x6
        self.__set_filled_squares(filled_squares)
        self.__set_matching_pairs(matching_pairs)
        self.__set_opposite_pairs(opposite_pairs)
        self._model = TangoModel(self.board_dims, self.filled_squares, self.matching_pairs, self.opposite_pairs)


    def __hash__(self) -> int:
        return hash((self._board_dims, self.__matching_pairs, self.__opposite_pairs, self.__filled_squares))


    @property
    def filled_squares(self) -> dict[tuple[int, int]: int]:
        """Return the squares that are already filled with a symbol."""
        return self.__filled_squares
    
    def __set_filled_squares(self, values:dict[tuple[int, int]: int]) -> None:
        if len(values) > len(self):
            msg = f"The number of filled squares exceeds the amount of board squares. Got {len(values)} filled squares."
            raise ValueError(msg)

        if not isinstance(values, dict):
            msg = f"filled_squares must be a dictionary. Got a {type(values).__name__} type instead."
            raise TypeError(msg)

        invalid_items = {
            square: value
            for square, value in values.items()
            if value != 1 and value != 0
        }
        if invalid_items:
            msg = (
                "The square values must be of binary type. "
                f"Got the following invalid values: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        self.__filled_squares = {square: (1 if value else 0) for square, value in values.items()}


    @property
    def matching_pairs(self) -> tuple[tuple[tuple[int, int], tuple[int, int]]] | None:
        return self.__matching_pairs
    
    def __set_matching_pairs(self, values:tuple[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
        if values is None:
            self.__matching_pairs = values
            return

        invalid_items = [pair for pair in values if not isinstance(pair, tuple) or len(pair) != 2]
        if invalid_items:
            msg = (
                "matching_pairs must be a collection of pairs of tuples."
                f" Got the following invalid pairs: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [square for pair in values for square in pair if not isinstance(square, tuple)]
        if invalid_items:
            msg = (
                "Squares in pair must be tuples of positive integers."
                f" Got the following invalid squares: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in values for square in pair for coord in square
            if not isinstance(coord, int) or coord < 1
        ]
        if invalid_items:
            msg = f"Coordinates must be positive integers. Got the following invalid squares: {invalid_items!r}."
            raise ValueError(msg)

        invalid_items = [pair for pair in values if super()._manhattan_distance(*pair) != 1]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)
        
        if not isinstance(values, tuple):
            self.__matching_pairs = tuple(values)
        else:
            self.__matching_pairs = values


    @property
    def opposite_pairs(self) -> tuple[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        Return the pairs of squares that are separated by a cross (×) sign, i.e.
        the squares that must have opposite symbols.
        """
        return self.__opposite_pairs
    
    def __set_opposite_pairs(self, value:tuple[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        if value is None:
            self.__opposite_pairs = value
            return

        invalid_items = [pair for pair in value if not isinstance(pair, tuple) or len(pair) != 2]
        if invalid_items:
            msg = (
                "opposite_pairs must be a collection of pairs of tuples."
                f" Got the following invalid pairs: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [square for pair in value for square in pair if not isinstance(square, tuple)]
        if invalid_items:
            msg = (
                "Squares in pair must be tuples of positive integers."
                f" Got the following invalid squares: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in value for square in pair for coord in square
            if not isinstance(coord, int) or coord < 1
        ]
        if invalid_items:
            msg = "Coordinates must be positive integers. Got the following invalid squares: {invalid_items!r}."
            raise ValueError(msg)

        invalid_items = [pair for pair in value if super()._manhattan_distance(*pair) != 1]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones."
                f" Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)
        
        if not isinstance(value, tuple):
            self.__opposite_pairs = tuple(value)
        else:
            self.__opposite_pairs = value


    @property
    def solution(self) -> dict[tuple[int, int]: bool] | None:
        if not self.is_solved:
            return None
        return self.board_squares

    def _set_solution(self, verbose:bool=False):
        nx.set_node_attributes(
            self._board,
            name="value",
            values={(i-1, j-1): round(pyo.value(self.model.x[i,j])) for i, j in self.model.S}
        )
        if verbose:
            print("Tango solution:")
            pprint(self.board_squares)


    def show(self) -> None:
        plt.figure(figsize=(3.4, 3.4))
        pos = {(i, j): (j, -i) for i, j in self.board.nodes()}
        nx.draw(
            self.board,
            pos= pos,
            with_labels= True,
            labels= nx.get_node_attributes(self.board, "value"),
            node_size= 1000,
            node_color= [
                "#EEEAE7" if (i+1,j+1) in self.filled_squares else "white"
                for (i, j) in self.board.nodes()
            ],
            node_shape="s",
            edgecolors="#EEEAE7",
            linewidths=1,
            width=0,
            edgelist=[
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.model.O] + [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.model.M
            ]
        )
        nx.draw_networkx_edge_labels(
            self._board,
            pos= pos,
            edge_labels= {
                ((i-1, j-1), (r-1,s-1)): "×" for i,j,r,s in self.model.O} | {
                ((i-1, j-1), (r-1,s-1)): "=" for i,j,r,s in self.model.M
            },
            font_color="#887658"
        )
        plt.show()
