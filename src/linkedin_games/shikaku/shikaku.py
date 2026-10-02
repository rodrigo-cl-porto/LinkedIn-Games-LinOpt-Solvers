from typing import Any

from .._shared.domain.game_facade import GameFacade
from ._game_grid import ShikakuGrid


class Shikaku(GameFacade):
    """The Shikaku game.
    
    A game grid with some numbered squares that states the rectangles' areas
        to be built on the grid.

    Objective:
        Partition the grid into non-overlapping rectangular figures so that each geometric shape
        covers the numbered square with a area that matches the number on its numbered square.
    
    Rules:
        - Each numbered square (seed) must be covered by only one rectangle that has a area equal to its number;
        - A rectangle must cover only one seed;
    """
    _game: ShikakuGrid

    def __init__(self,
            size: int,
            seeds: dict[tuple[int, int], dict[str, Any] | int | None]
        ) -> None:
        """
        Args:
            size: The side length of the game.
            seeds: Rectangle seeds on grid as a dictionary of items as
                `(row, column) : area` or as `(row, column) : {"color": str, "area": int}`.
        
        Raises:
            TypeError: if type inputs are not respected.
            ValueError: If there are some seeds with the same color.
        """
        super().__init__(size, seeds)

    def _set_game(self, seeds: dict[tuple[int, int], dict[str, Any] | int | None]) -> None:
        self._game = ShikakuGrid(dims=self.dims, seeds=seeds)

    @property
    def seeds(self) -> dict[str, dict[str, Any]]:
        """The seeds of the game.

        Returns:
            All the information about the seeds.
        """
        return self._game.seeds

    @property
    def solution(self) -> list[dict[str, tuple[int, int]]]:
        """All rectangles that solves the Patches game.

        Returns:
            The solving rectangles as a list of dictionaries in the format
                `{"color_code": color_code, "top_left": (top, left), "dims": (height, width)}`.
        """
        return self._game.solution
