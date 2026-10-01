from .._shared.domain.game_facade import GameFacade
from ._game_grid import QueensGrid


class Queens(GameFacade):
    """The [LinkedIn Queens](https://www.linkedin.com/games/queens/) game.
    
    A game grid with colored regions intended to put crowns on it.

    Objective:
        To place a crown in each row, column, and colored region on the grid.

    Rules:
        - There can only be one crown in each row, column and colored region;
        - There cannot be adjacent crowns, not even along adjacent diagonals.
    """
    _game: QueensGrid

    def __init__(self,
            size: int,
            regions: dict[str, set[tuple[int, int]]] | list[set[tuple[int, int]]]
        ) -> None:
        """
        Args:
            size: The side length of the game.
            regions: Regions as a dictionary of `color: {(row, column), ...}` items.
        """
        super().__init__(size, regions)

    def _set_game(self, regions: dict[str, set[tuple[int, int]]] | list[set[tuple[int, int]]]) -> None:
        self._game = QueensGrid(dims=self.dims, regions=regions)

    @property
    def regions(self) -> dict[str, set[tuple[int, int]]]:
        """All colored regions on the grid.

        It's assumed that the regions are non-overlapping and cover the entire grid.

        Returns:
            The set of all colored regions on the grid.
        """
        return self._game.regions

    @property
    def solution(self) -> list[tuple[int, int]]:
        """The crowned squares of Queens game.
        
        Returns:
            Locations of all crowns as a list of squares as `(row, column)`
            or an empty list if the game is not solved yet.
        """
        return self._game.crowns
