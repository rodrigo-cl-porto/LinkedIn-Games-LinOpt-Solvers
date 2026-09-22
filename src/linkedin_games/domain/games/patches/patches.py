from typing import Any

from ..base.shikaku.shikaku import Shikaku
from ._model import PatchesModel
from ._patch_seed import PatchSeed


class Patches(Shikaku):
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
    def __init__(self, size:int, seeds: dict[tuple[int, int], int | dict[str, Any] | None]) -> object:
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


    def _set_model(self) -> None:
        self._model = PatchesModel(self.grid_dims, self.seeds)


    @staticmethod
    def _build_seeds(seeds: dict[tuple[int, int], int | dict[str, Any] | None]) -> list[PatchSeed]:
        return [
            PatchSeed(
                square=square,
                color=seed.get("color") if isinstance(seed, dict) else None,
                area=seed if isinstance(seed, int) else seed.get("area") if isinstance(seed, dict) else None,
                shape=seed.get("shape") if isinstance(seed, dict) else None
            ) for square, seed in seeds.items()
        ]
