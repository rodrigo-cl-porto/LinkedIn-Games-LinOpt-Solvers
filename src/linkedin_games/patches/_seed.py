from typing import Any

from .._shared.utils.is_perfect_square import IsPerfectSquare
from ..shikaku._seed import RectangleSeed
from ._shape import PatchShape


class PatchSeed(RectangleSeed):
    """A seed that creates a patch in the Patches game."""

    def __init__(self,
            square: tuple[int, int],
            color: str | None = "#FFFFFF",
            area: int | None = None,
            shape: str | None = PatchShape.ANY,
        ) -> None:
        """
        Args:
            square: The board position of the seed as a `(row, column)` tuple.
            area: The required area of the patch to be built.
            shape: The patch's required shape.
            color: The seed's color name or its hex code as a `#RRGGBB` string.
        """
        self._set_shape(shape)
        if area is None:
            super().__init__(square, color)
            self._set_area(None)
        else:
            super().__init__(square, color, area)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"square={self.square},\n\t"
            f"shape={type(self.shape).__name__}.{self.shape},\n\t"
            f"area={self.area},\n\t"
            f"color_code={self.color_code}\n)"
        )

    def __str__(self) -> str:
        return (
            f"A Patches seed square located at {self.square}"
            f" that creates a {self.color}"
            f" {self.shape.lower() + " "
            if self.shape != PatchShape.ANY else ""}rectangle"
            f" with{f" a required area of {self.area} squares"
            if self.area is not None else "out any required area"}."
        )

    def __hash__(self) -> int:
        return hash((self.color_code, self.square, self.shape, self.area))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PatchSeed):
            return False
        return (
            self.color_code == other.color_code
            and self.square == other.square
            and self.area == other.area
            and self.shape == other.shape
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "color": self.color,
            "color_code": self.color_code,
            "square": self.square,
            "shape": self.shape,
            "area": self.area
        }

    @property
    def shape(self) -> str:
        """The patch's required shape.

        Returns:
            The patch shape's name required by the seed square.
        """
        return str(self.__shape)

    def _set_shape(self, value: str | None = PatchShape.ANY) -> None:

        if value is None:
            self.__shape = PatchShape.ANY
            return
        
        if not isinstance(value, str):
            msg = f"The patch shape must be a string. Got a {type(value).__name__} instead."
            raise TypeError(msg)
        
        try:
            self.__shape = PatchShape(value.strip().lower())
        except ValueError as exc:
            valid_shapes = f"'{"', '".join(str(shape) for shape in PatchShape)}'"
            msg = f"'{value}' is not a valid rectangle shape. Please, input one of theses shapes: {valid_shapes}"
            raise ValueError(msg) from exc

    @property
    def area(self) -> int | None:
        """The required rectangle's area.
        
        Returns:
            The patch's area required by the seed or `None` if the seed doesn't claim it.
        """
        return self._area

    def _set_area(self, value: int | None = None) -> None:

        if value is None:
            self._area = None
            return

        if not isinstance(value, int):
            msg = f"The required area must be an integer or None. Got {type(value).__name__} instead."
            raise TypeError(msg)

        if value < 1:
            msg = f"The required area must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)

        if self.shape == PatchShape.SQUARE and not IsPerfectSquare.check(value):
            msg = f"The required area ({value!r}) is not a perfect square."
            raise ValueError(msg)

        self._area = value
