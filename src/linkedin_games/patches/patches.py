from typing import Any

from .._shared.domain.game_facade import GameFacade
from ._game_grid import PatchesGrid


class Patches(GameFacade):
    """
    The [LinkedIn Patches](https://www.linkedin.com/games/patches/) game.
    
    A game grid with some colored rectangle seeds that may state some features about the rectangles
        to be built on the grid, such as a required area (optional) or a required shape
        (which can be a `vertical` rectangle, a `horizontal` rectangle, a `square` or any shape).

    Objective:
        Partition the grid into non-overlapping rectangular patches so that each patch meets
        the prescriptions on their respective seeds.
    
    Rules:
        - Each seed must be covered by only one rectangle that attends its prescriptions;
        - A rectangle must cover only one seed;
        - The area of all rectangles must be greater than 1 square on the grid.
    """

    def __init__(self,
            size: int,
            seeds: dict[tuple[int, int], dict[str, Any] | int | None]
        ) -> None:
        """
        Args:
            size: The side length of the game.
            seeds: Rectangle seeds on grid as a dictionary of items as:
                ```python
                (row, column) : {
                    "color": str | None, # optional
                    "area": int | None, # optional
                    "shape": Literal[ # optional
                        "vertical",
                        "horizontal",
                        "square",
                        "any"
                    ] | None
                } | None
                ```
        
        Raises:
            TypeError: if type inputs are not respected.
            ValueError: If there are some seeds with the same color.
        """
        super().__init__()
        self._game = PatchesGrid(grid_dims=(size, size), seeds=seeds)
