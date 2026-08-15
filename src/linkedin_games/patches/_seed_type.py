from typing import TypedDict, Literal

from ._patch_shape import PatchShape

class Seed(TypedDict, total=False):
    color: str | None
    area: int | None
    shape: Literal[
        PatchShape.VERTICAL,
        PatchShape.HORIZONTAL,
        PatchShape.SQUARE,
        PatchShape.ANY
    ] | None
