from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._game_board import GameBoard
from ._model import QueensModel
from ._region import Region


class Queens(GameBoard):
    """
    The [LinkedIn Queens](https://www.linkedin.com/games/queens/) game.
    
    A game board with colored regions intended to put crowns on it.

    Objective:
        To place a crown in each row, column, and colored region on the board.

    Rules:
        - There can only be one crown in each row, column and colored region;
        - There cannot be adjacent crowns, not even along adjacent diagonals.
    """

    def __init__(self, board_dims: tuple[int, int], regions: dict[str, set[tuple[int, int]]]) -> None:
        """
        Args:
            board_dims: Board dimensions as a `(rows, columns)` tuple.
            regions: Regions as a dictionary of `color: {(row, column), ...}` items.
        """
        super().__init__(board_dims)
        self.__set_regions(regions)
        self._model = QueensModel(self.board_dims, self.regions)


    def __hash__(self) -> int:
        return hash((self._board_dims, self.__regions))


    @property
    def regions(self) -> dict[str, set[tuple[int, int]]]:
        """All colored regions on the board.

        It's assumed that the regions are non-overlapping and cover the entire board.

        Returns:
            The set of all colored regions on the board.
        """
        return {region.color_code: region.squares for region in self.__regions}

    def __set_regions(self, regions:dict[str, set[tuple[int, int]]]) -> None:

        if not isinstance(regions, dict):
            msg = "regions must be a dict of Region classes."
            raise TypeError(msg)

        if len(regions) < 1:
            msg = "The set of Regions cannot be empty!"
            raise ValueError(msg)

        all_region_squares = [square for squares in regions.values() for square in squares]
        overlapping_squares = {square for square in all_region_squares if all_region_squares.count(square) > 1}
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

        self.__regions = {Region(color=color, squares=squares) for color, squares in regions.items()}

        nx.set_node_attributes( # Adding a color for each square on the board
            self._board,
            name="color",
            values={(i-1, j-1): region.color for region in self.__regions for (i, j) in region.squares}
        )


    @property
    def crowns(self) -> list[tuple[int, int]] | None:
        """
        The crowned squares of Queens game.

        Returns:
            Locations of all crowns as a list of squares as `(row, column)`
            or `None` if the game is not solved yet.
        """
        if not self.is_solved:
            return None
        return sorted((i+1, j+1) for (i, j) in self.__crowns.nodes())


    def _set_solution(self, verbose:bool = False) -> None:
        nx.set_node_attributes(
            self.board,
            name="value",
            values={(i-1, j-1): round(pyo.value(self.model.x[i, j])) for (i, j) in self.model.S}
        )
        crowns = [square for square, value in nx.get_node_attributes(self.board, "value").items() if value == 1]
        self.__crowns = self.board.subgraph(crowns)
        if verbose:
            print("These are the squares that contain a crown:")
            pprint(self.crowns)


    def show(self) -> None:
        """Show the Queens' board."""
        plt.figure(figsize=(3.4, 3.4))
        nx.draw(
            self.board,
            pos={(i, j): (j, -i) for i, j in self.board.nodes()},
            with_labels=True,
            labels=dict.fromkeys(self.__crowns.nodes(), "O"),
            node_size=1000,
            node_color=list(nx.get_node_attributes(self.board, "color").values()),
            node_shape="s", # Squared-shape nodes
            width=0
        )
        plt.show()
