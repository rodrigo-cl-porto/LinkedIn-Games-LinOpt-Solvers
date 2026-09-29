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
        super().__init__()
        self._game = ZipGrid(
            grid_dims=(size, size),
            numbered_squares=numbered_squares, walls=walls
        )
