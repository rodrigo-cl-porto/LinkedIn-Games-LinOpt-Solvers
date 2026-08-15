from typing import Literal

from ..shikaku.shikaku import Shikaku
from ._model import PatchesModel
from ._patch_seed import PatchSeed
from ._seed_type import Seed


class Patches(Shikaku):
    """
    The [LinkedIn Patches](https://www.linkedin.com/games/patches/) game.
    
    A game board with some colored rectangle seeds that may state some features about the rectangles
        to be built on the board, such as a required area (optional) or a required shape
        (which can be a `vertical` rectangle, a `horizontal` rectangle, a `square` or any shape).

    Objective:
        Partition the board into non-overlapping rectangular patches so that each patch meets
        the prescriptions on their respective seeds.
    
    Rules:
        - Each seed must be covered by only one rectangle that attends its prescriptions;
        - A rectangle must cover only one seed;
        - The area of all rectangles must be greater than 1 square on the board.
    """
    def __init__(self, size:int, seeds: dict[tuple[int, int], Seed | None]) -> object:
        """
        Args:
            size: The side length of the game.
            seeds: Rectangle seeds on board as a dictionary of items as:
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


    @property
    def seeds(self) -> dict[tuple[int, int], dict[Literal["color", "shape", "area"], str | int | None]]:
        """
        The seeds of the game.
        
        Returns:
            All the information about the seeds as a dictionary of items as
                ```python
                (row: int, column: int): {
                    "color": str       # color name or hex code as #RRGGBB,
                    "area": int | None # required area,
                    "shape": Literal[  # rectangle shape
                        "vertical",
                        "horizontal",
                        "square",
                        "any"
                    ]
                }
                ```
        """
        return {
            seed.square : {
                "color": seed.color_code,
                "shape": seed.shape,
                "area": seed.area
            } for seed in self._seeds
        }


    def _set_model(self) -> None:
        self._model = PatchesModel(self.board_dims, self._seeds)


    @staticmethod
    def _build_rectangle_seed_list(seeds: dict[tuple[int, int], int | Seed | None]) -> list[PatchSeed]:
        return [
            PatchSeed(
                square=square,
                color=seed.get("color") if seed is not None else None,
                area=seed if isinstance(seed, int) else seed.get("area") if isinstance(seed, dict) else None,
                shape=seed.get("shape") if seed is not None else None
            ) for square, seed in seeds.items()
        ]
