from typing import Any

from .._shared.optimization.solution._solution import GameSolution
from ..shikaku._game_grid import ShikakuGrid
from ._seed import PatchSeed
from ._shape import PatchShape
from ._solution import PatchesSolution


class PatchesGrid(ShikakuGrid):
    
    def __init__(self, grid_dims: tuple[int, int], seeds: dict[tuple[int, int], dict[str, Any] | int | None]) -> None:
        super().__init__(grid_dims, seeds)


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


    def set_solution(self, value: GameSolution) -> None:

        if not isinstance(value, PatchesSolution):
            msg = f"Invalid input. Got a {type(value).__name__} object."
            raise TypeError(msg)

        for seed_color, rectangle in value.rectangles.items():
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
