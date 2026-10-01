from ..shikaku._seed_type import SeedType
from ..shikaku.shikaku import Shikaku
from ._game_grid import PatchesGrid
from ._seed_type import PatchSeedType


class Patches(Shikaku):
    """The [LinkedIn Patches](https://www.linkedin.com/games/patches/) game.
    
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
    def __init__(self, size: int, seeds: dict[tuple[int, int], PatchSeedType | int | None]) -> None:
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
        super().__init__(size, seeds)

    def _set_game(self, seeds: dict[tuple[int, int], SeedType | int | None]) -> None:
        self._game = PatchesGrid(dims=self.dims, seeds=seeds)
