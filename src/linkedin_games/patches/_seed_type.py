from typing import TypedDict, Literal

from ._rectangle_shape import RectangleShape

class Seed(TypedDict, total=False):
    color: str | None
    area: int | None
    shape: Literal[
        RectangleShape.VERTICAL,
        RectangleShape.HORIZONTAL,
        RectangleShape.SQUARE,
        RectangleShape.ANY
    ] | None
