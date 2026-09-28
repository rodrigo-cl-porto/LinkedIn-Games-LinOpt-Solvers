from typing import Any

from ....optimization.solutions._solution import GameSolution
from ..shikaku.shikaku import Shikaku
from ._patch_seed import PatchSeed
from ._patch_shape import PatchShape


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
    
    def __init__(self, size:int, seeds: dict[tuple[int, int], dict[str, Any] | int | None]) -> None:
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


    @staticmethod
    def _build_seeds(seeds: dict[tuple[int, int], dict[str, Any] | int | None]) -> list:
        return [
            PatchSeed(
                square=square,
                color=seed.get("color") if isinstance(seed, dict) else None,
                area=seed if isinstance(seed, int) else seed.get("area") if isinstance(seed, dict) else None,
                shape=seed.get("shape") if isinstance(seed, dict) else None
            ) for square, seed in seeds.items()
        ]


    @Shikaku.solution.setter
    def solution(self, value: GameSolution) -> None:

        if not isinstance(value, GameSolution):
            raise TypeError(f"Invalid input. Got {type(value).__name__} instead of GameSolution.")

        for seed_color, rectangle in value.get("rectangles").items():
            seed= self._seeds[seed_color].to_dict()
            patch_area =  rectangle.height * rectangle.width
            if seed["area"] is not None and patch_area != seed["area"]:
                msg = f"The patch's area ({patch_area}) doesn't attend to the required area ({seed["area"]})."
                raise ValueError(msg)
            
            match seed["shape"]:
                case PatchShape.VERTICAL:
                    if rectangle.height <= rectangle.width:
                        msg = (
                            f"The patch doesn't have {seed["shape"].lower} shape."
                            f" Its height ({rectangle.height!r}) should be"
                            f" greater than its width ({rectangle.width!r})."
                        )
                        raise ValueError(msg)
                
                case PatchShape.HORIZONTAL:
                    if rectangle.height >= rectangle.width:
                        msg = (
                            f"The patch doesn't have {seed["shape"].lower} shape."
                            f" Its width ({rectangle.width!r}) should be"
                            f" greater than its height ({rectangle.height!r})."
                        )
                        raise ValueError(msg)
                
                case PatchShape.SQUARE:
                    if rectangle.height != rectangle.width:
                        msg = (
                            f"The patch doesn't have {seed["shape"].lower} shape."
                            f" Its height ({rectangle.height!r}) should be"
                            f" equal to its width ({rectangle.width!r})."
                        )
                        raise ValueError(msg)
        
        self._solution = value
