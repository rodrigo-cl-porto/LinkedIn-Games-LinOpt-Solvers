from typing import Any

from .._core._color import Color
from ._rectangle import Rectangle


class RectangleSeed:
    """A seed that creates a rectangle in the Patches game."""

    def __init__(self,
            square: tuple[int, int],
            color: str | None = "#FFFFFF",
            area: int = 1
        ) -> object:
        """
        Args:
            square: The grid position of the seed as a `(row, column)` tuple.
            area: The required area of the rectangle to be built.
            color: The seed's color name or its hex code as a `#RRGGBB` string.
        """
        self.__set_square(square)
        self.__color = Color(color)
        self._set_area(area)
        self._rectangle: Rectangle


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"square={self.square},\n\t"
            f"area={self.area},\n\t"
            f"color_code={self.color_code}\n)"
        )


    def __str__(self) -> str:
        return (
            f"A {type(self).__name__} seed located at square {self.square}"
            f" that creates a {self.color} rectangle"
            f" with{f" a required area of {self.area} squares"
            if self.area is not None else "out any required area"}."
        )


    def __hash__(self) -> int:
        return hash((self.color_code, self.square, self.area))


    def __len__(self) -> int:
        return 1


    def __abs__(self) -> int:
        return 1


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RectangleSeed):
            return False
        return (
            self.color_code == other.color_code
            and self.square == other.square
            and self.area == other.area
        )


    def __ne__(self, other:object) -> bool:
        return not self.__eq__(other)


    def to_dict(self) -> dict[str, Any]:
        return {
            "color_code": self.color_code,
            "color": self.color,
            "square": self.square,
            "area": self.area
        }


    @property
    def square(self) -> tuple[int, int]:
        """
        Board square where the seed lies.
        
        Returns:
            Board square of the rectangle seed as a `(row, column)` tuple.
        """
        return self.__square

    def __set_square(self, value: tuple[int, int]) -> None:

        if not isinstance(value, tuple):
            msg = f"Seed square must be a tuple. Got a {type(value).__name__} type instead."
            raise TypeError(msg)
        
        if len(value) != 2:
            msg = f"Seed square must be a pair (m,n). Got a tuple with length {len(value)}."
            raise ValueError(msg)
        
        if (any(not isinstance(coord, int) or isinstance(coord, bool) or coord < 1 for coord in value)):
            msg = f"Seed square coordinates must be positive integers. Got {value!r} instead."
            raise ValueError(msg)
        
        self.__square = value


    @property
    def area(self) -> int:
        """
        The required rectangle's area.
        
        Returns:
            The rectangle's area required by the seed or `None` if the seed doesn't claim it.
        """
        return self._area

    def _set_area(self, value: int=1) -> None:

        if value is None:
            self._area = 1
            return
        
        if not isinstance(value, int):
            msg = f"The required area must be an integer or None. Got {type(value).__name__} instead."
            raise TypeError(msg)

        if value < 1:
            msg = f"The required area must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)

        self._area = value
        self._area = value


    @property
    def color(self) -> str:
        """
        The name of the seed's color.

        Returns:
            The color's name of the rectangle.
        """
        return self.__color.name
    
    @color.setter
    def color(self, value:str) -> None:
        self.__color.color = value


    @property
    def color_code(self) -> str:
        """
        The code of seed's color.

        Returns:
            Hex code color as a `"#RRGGBB"` string.
        """
        return self.__color.hex_code
    
    @color_code.setter
    def color_code(self, value:str) -> None:
        self.__color.hex_code = value


    @property
    def rectangle(self) -> Rectangle:
        """
        The seed's created rectangle.
        
        Returns:
            The rectangle created by the seed after solving the game.
        """
        return self._rectangle

    @rectangle.setter
    def rectangle(self, value: dict[str, int]) -> None:

        rectangle_area =  value["height"] * value["width"]
        if self.area is not None and rectangle_area != self.area:
            msg = f"The rectangle's area ({rectangle_area}) doesn't attend to the required area ({self.area})."
            raise ValueError(msg)

        self._rectangle = Rectangle(
            top_left=(value["top"], value["left"]),
            dims=(value["height"], value["width"])
        )
