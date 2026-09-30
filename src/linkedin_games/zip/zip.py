from .._shared.domain.game_facade import GameFacade
from ._game_grid import ZipGrid


class Zip(GameFacade):
    """
    The [LinkedIn Zip](https://www.linkedin.com/games/zip/) game.
    
    A game grid with some numbered squares and walls (walls are optional).
    
    Objective:
        To trace a single path that runs through all the grid squares.

    Rule:
        The path must move through numbered squares in ascending order,
        starting from square number 1 to the one with the highest number.
    """

    _game: ZipGrid

    def __init__(self,
            size: int,
            numbered_squares: list[tuple[int, int]],
            walls: list[tuple[tuple[int, int], tuple[int, int]]] | None = None
        ) -> None:
        """
        Args:
            size: The side length of the game.
            numbered_squares: Squares with a assigned number as a dictionary of `(row, column): number` items.
            walls: Pairs of squares separated by a walls as a set of `((row1, column1), (row2, column2))`.
        
        Raises:
            TypeError: If the types of the arguments don't match their required types.
            ValueError: If the quantity of numbered squares exceeds the total number of squares on the grid,
                or if the number of walls exceeds the total number of edges on the grid,
                or if any pair of squares in walls are not adjacent.
        """
        self._game = ZipGrid(
            grid_dims=(size, size),
            numbered_squares=numbered_squares,
            walls=walls
        )


    @property
    def numbered_squares(self) -> list[tuple[int, int]]:
        """
        The squares with a assigned number.

        Returns:
            The numbered squares as a dictionary of `(row, column): number` items.
        """
        return self._game.numbered_squares


    @property
    def walls(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        The pairs of squares separated by a wall.
        
        Returns:
            All the grid edges blocked by a wall as a tuple of `((row1, column1), (row2, column2))`.
        """
        return self._game.walls


    @property
    def grid_edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        """
        All the grid edges and their respective assigned values (if any).
        
        Returns:
            All edges as a dictionary of `((row1, column1), (row2, column2)): value` items.
        """
        return self._game.grid_edges


    @property
    def path(self) -> list[tuple[int, int]]:
        """
        The solving path of Zip game.
        
        The path that visits all the grid squares, starting from 1-numbered squared to the highest-numbered square.

        Returns:
            The solving path as a list of squares as `(row, column)`.
        """
        return self._game.path
