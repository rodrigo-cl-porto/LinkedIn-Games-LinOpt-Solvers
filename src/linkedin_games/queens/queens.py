from .._shared.domain.game_facade import GameFacade
from ._game_grid import QueensGrid


class Queens(GameFacade):
    """
    The [LinkedIn Queens](https://www.linkedin.com/games/queens/) game.
    
    A game grid with colored regions intended to put crowns on it.

    Objective:
        To place a crown in each row, column, and colored region on the grid.

    Rules:
        - There can only be one crown in each row, column and colored region;
        - There cannot be adjacent crowns, not even along adjacent diagonals.
    """

    def __init__(self,
            size: int,
            regions: dict[str, set[tuple[int, int]]] | list[set[tuple[int, int]]]
        ) -> None:
        """
        Args:
            size: The side length of the game.
            regions: Regions as a dictionary of `color: {(row, column), ...}` items.
        """
        self._game = QueensGrid(grid_dims=(size, size), regions=regions)
