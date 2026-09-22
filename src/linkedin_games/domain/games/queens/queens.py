from ..._game_grid import GameGrid
from ._region import Region


class Queens(GameGrid):
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
        self.__set_regions(regions)


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
            colors = generate_hex_codes(len(regions))
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
