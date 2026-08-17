from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from .._core._game_grid import GameGrid
from .._mixin._color_generator_mixin import ColorGeneratorMixin
from ._model import QueensModel
from ._region import Region


class Queens(ColorGeneratorMixin, GameGrid):
    """
    The [LinkedIn Queens](https://www.linkedin.com/games/queens/) game.
    
    A game grid with colored regions intended to put crowns on it.

    Objective:
        To place a crown in each row, column, and colored region on the grid.

    Rules:
        - There can only be one crown in each row, column and colored region;
        - There cannot be adjacent crowns, not even along adjacent diagonals.
    """

    def __init__(self, size:int, regions: dict[str, set[tuple[int, int]]] | list[set[tuple[int, int]]]) -> None:
        """
        Args:
            size: The side length of the game.
            regions: Regions as a dictionary of `color: {(row, column), ...}` items.
        """
        super().__init__(grid_dims=(size, size))
        self.__crowns: nx.Graph
        self.__set_regions(regions)
        self._model = QueensModel(self.grid_dims, self.regions)


    def __hash__(self) -> int:
        return hash((self._grid_dims, self.__regions))


    @property
    def size(self) -> int:
        """The side length of the game.

        Returns:
            The number of rows (or columns) on game's grid.
        """
        return self.grid_dims[0]


    @property
    def regions(self) -> dict[str, set[tuple[int, int]]]:
        """All colored regions on the grid.

        It's assumed that the regions are non-overlapping and cover the entire grid.

        Returns:
            The set of all colored regions on the grid.
        """
        return {region.color_code: region.squares for region in self.__regions}

    def __set_regions(self, regions:dict[str, set[tuple[int, int]]] | list[set[tuple[int, int]]]) -> None:

        if not isinstance(regions, (dict, list)):
            msg = f"regions must be a dict or list. Got {type(regions).__name__} instead."
            raise TypeError(msg)

        if len(regions) < 1:
            msg = "regions cannot be empty!"
            raise ValueError(msg)

        if isinstance(regions, list):
            colors = super()._generate_hex_codes(len(regions))
            regions = dict(zip(colors, regions, strict=True))

        all_region_squares = [square for squares in regions.values() for square in squares]
        overlapping_squares = {square for square in all_region_squares if all_region_squares.count(square) > 1}
        if overlapping_squares:
            msg = f"The regions must not overlap each other. Overlapping squares: {overlapping_squares}"
            raise ValueError(msg)

        all_region_squares = set(all_region_squares)
        if all_region_squares != self.grid_squares:
            if len(all_region_squares) > len(self):
                squares_not_in_grid = all_region_squares - self.grid_squares.keys()
                msg = (
                    "The regions must cover the entire grid and must not go beyond the grid's boundaries."
                    f" Squares outside the grid: {squares_not_in_grid!r}"
                )
                raise ValueError(msg)

            if len(all_region_squares) < len(self):
                missing_squares = self.grid_squares.keys() - all_region_squares
                msg = (
                    "The regions must cover the entire grid and must not go beyond the grid's boundaries."
                    f" Squares not in an region: {missing_squares!r}"
                )
                raise ValueError(msg)

        self.__regions = [Region(color=color, squares=squares) for color, squares in regions.items()]

        nx.set_node_attributes( # Adding a color for each square on the grid
            self._grid,
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

        x = self.model.x
        S = self.model.S
        nx.set_node_attributes(
            self.grid,
            name="value",
            values={(i-1, j-1): round(pyo.value(x[i, j])) for (i, j) in S}
        )

        crowns = [square for square, value in nx.get_node_attributes(self.grid, "value").items() if value == 1]
        self.__crowns = self.grid.subgraph(crowns)
        
        if verbose:
            print("These are the squares that contain a crown:")
            pprint(self.crowns)


    def show(self) -> None:
        """Show the Queens' grid."""
        width = height = self.size * 0.5
        plt.figure(figsize=(width, height))
        nx.draw(
            self.grid,
            pos={(i, j): (j, -i) for i, j in self.grid.nodes()},
            with_labels=True,
            arrows=False,
            labels=
                dict.fromkeys(self.__crowns.nodes(), "O") if self.__crowns is not None
                else dict.fromkeys(self.grid.nodes(), ""),
            node_size=1100,
            node_color=list(nx.get_node_attributes(self.grid, "color").values()),
            node_shape="s", # Squared-shape nodes
            width=0,
            edgecolors="black",
            linewidths=.5
        )
        plt.show()
