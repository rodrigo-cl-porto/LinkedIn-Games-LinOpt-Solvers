from pprint import pprint
from typing import Self

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._game_board import GameBoard
from ._model import QueensModel
from ._region import Region


class Queens(GameBoard):
    """A Queens is board game with colored regions
    
    Attributes:
        board (nx.Graph): The board of the game.
        board_dims (tuple[int, int]): The dimensions of the board as (rows, columns).
        board_edges (set[tuple[tuple[int, int], tuple[int, int]]]): The set of all edges on the board.
        board_squares (set[tuple[int, int]]): The set of all squares on the board.
        regions (set[Region]): The set of colored regions on the board.
        crowns (tuple[tuple[int, int]]): The crowned squares of the game.
        is_solved (bool): Whether the game has been solved or not.
        model (pyo.ConcreteModel): The linear optimization model for the game.
        regions (set[Region]): The set of colored regions on the board.
    
    Methods:
        show (None): Show the game board with the solution.
        solve (None): Solve the game using linear optimization.
    """

    def __init__(self, board_dims:tuple[int, int], regions:dict[str, set[tuple[int, int]]]) -> Self:
        super().__init__(board_dims)
        self._set_regions(regions)
        self._model = QueensModel(self.board_dims, self.regions)

    def __hash__(self):
        return hash((self._board_dims, self._regions))


    @property
    def regions(self) -> set[Region]:
        """All colored regions on the board.

        It's assumed that the regions are non-overlapping and cover the entire board.
        
        Returns:
            The set of colored regions on the board.
        """
        return self._regions

    def _set_regions(self, regions:dict[str, set[tuple[int, int]]]) -> None:

        if not isinstance(regions, dict):
            msg = "regions must be a dict of Region classes."
            raise TypeError(msg)

        if len(regions) < 1:
            msg = "The set of Regions cannot be empty!"
            raise ValueError(msg)

        all_region_squares = [square for squares in regions.values() for square in squares]
        overlapping_squares = {
            square for square in all_region_squares
            if all_region_squares.count(square) > 1
        }
        if overlapping_squares:
            msg = (
                "The regions must not overlap each other."
                f" Overlapping squares: {overlapping_squares}"
            )
            raise ValueError(msg)

        all_region_squares = set(all_region_squares)
        if all_region_squares != self.board_squares:
            if len(all_region_squares) > len(self):
                squares_not_in_board = all_region_squares - self.board_squares.keys()
                msg = (
                    "The regions must cover the entire board"
                    " and must not go beyond the board's boundaries."
                    f" Squares outside the board: {squares_not_in_board!r}"
                )
                raise ValueError(msg)

            if len(all_region_squares) < len(self):
                missing_squares = self.board_squares.keys() - all_region_squares
                msg = (
                    "The regions must cover the entire board"
                    " and must not go beyond the board's boundaries."
                    f" Squares not in an region: {missing_squares!r}"
                )
                raise ValueError(msg)

        self._regions = {Region(color=color, squares=squares) for color, squares in regions.items()}

        nx.set_node_attributes( # Adding a color for each square on the board
            self._board,
            name="color",
            values={
                (i-1, j-1): region.color for region in self.regions for (i, j) in region.squares
            }
        )

    @property
    def solution(self) -> list[tuple[int, int]] | None:
        """List of squares that contain a crown.
        
        Returns:
            A sorted tuple of squares that contain a crown.
        """
        if not self.is_solved:
            return None
        return sorted((i+1, j+1) for (i, j) in self.__crowns.nodes())

    def _set_solution(self, verbose: bool = False) -> None:
        nx.set_node_attributes(
            self.board,
            name="value",
            values={(i-1, j-1): round(pyo.value(self.model.x[i, j])) for (i, j) in self.model.S}
        )
        crowns = [
            square for square, value in nx.get_node_attributes(self.board, "value").items()
            if value == 1
        ]
        self.__crowns = self.board.subgraph(crowns)
        if verbose:
            print("These are the squares that contain a crown:")
            pprint(self.solution)

    def show(self) -> None:
        plt.figure(figsize=(3.4, 3.4))
        nx.draw(
            self.board,
            pos={(i, j): (j, -i) for i, j in self.board.nodes()},
            with_labels=True,
            labels={square: "O" for square in self.__crowns.nodes()},
            node_size=1000,
            node_color=[color for color in nx.get_node_attributes(self.board, "color").values()],
            node_shape="s", # Squared-shape nodes
            width=0
        )
        plt.show()
