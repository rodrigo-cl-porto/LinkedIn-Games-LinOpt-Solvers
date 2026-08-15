from typing import Any

from .._mixin._is_perfect_square_mixin import IsPerfectSquareMixin
from ..shikaku._rectangle import Rectangle
from ..shikaku._rectangle_seed import RectangleSeed
from ._patch_shape import PatchShape


class PatchSeed(IsPerfectSquareMixin, RectangleSeed):
    """A seed that creates a patch in the Patches game."""

    def __init__(self,
            square: tuple[int, int],
            color: str | None = "#FFFFFF",
            area: int | None = None,
            shape: str | None = PatchShape.ANY,
        ) -> object:
        """
        Args:
            square: The board position of the seed as a `(row, column)` tuple.
            area: The required area of the patch to be built.
            shape: The patch's required shape.
            color: The seed's color name or its hex code as a `#RRGGBB` string.
        """
        self.__set_shape(shape)
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
        """
        The patch's required shape.

        Returns:
            The patch shape's name required by the seed square.
        """
        return str(self.__shape)

    def __set_shape(self, value:str|None) -> None:

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
        """
        The required rectangle's area.
        
        Returns:
            The patch's area required by the seed or `None` if the seed doesn't claim it.
        """
        return self._area

    def _set_area(self, value: int | None) -> None:

        if value is None:
            self._area = None
            return

        if not isinstance(value, int):
            msg = f"The required area must be an integer or None. Got {type(value).__name__} instead."
            raise TypeError(msg)

        if value < 1:
            msg = f"The required area must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)

        if self.shape == PatchShape.SQUARE and not PatchSeed._is_perfect_square(value):
            msg = f"The required area ({value!r}) is not a perfect square."
            raise ValueError(msg)

        self._area = value



    @property
    def patch(self) -> Rectangle:
        """
        The created patch.
        
        Returns:
            The patch created by the seed after solving the game.
        """
        return self._rectangle

    @patch.setter
    def patch(self, value: dict[str, int]) -> None:

        patch_area =  value["height"] * value["width"]
        if self.area is not None and patch_area != self.area:
            msg = f"The patch's area ({patch_area}) doesn't attend to the required area ({self.area})."
            raise ValueError(msg)
        
        match self.shape:
            case PatchShape.VERTICAL:
                if value["height"] <= value["width"]:
                    msg = (
                        f"The patch doesn't have {self.shape.lower} shape."
                        f" Its height ({value["height"]!r}) should be greater than its width ({value["width"]!r})."
                    )
                    raise ValueError(msg)
            
            case PatchShape.HORIZONTAL:
                if value["height"] >= value["width"]:
                    msg = (
                        f"The patch doesn't have {self.shape.lower} shape."
                        f" Its width ({value["width"]!r}) should be greater than its height ({value["height"]!r})."
                    )
                    raise ValueError(msg)
            
            case PatchShape.SQUARE:
                if value["height"] != value["width"]:
                    msg = (
                        f"The patch doesn't have {self.shape.lower} shape."
                        f" Its height ({value["height"]!r}) should be equal to its width ({value["width"]!r})."
                    )
                    raise ValueError(msg)

        self._rectangle = Rectangle(
            top_left=(value["top"], value["left"]),
            dims=(value["height"], value["width"])
        )
