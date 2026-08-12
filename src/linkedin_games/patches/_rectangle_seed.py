from typing import Any
from math import sqrt

from ..core._color import Color
from ._rectangle import Rectangle
from ._rectangle_shape import RectangleShape


class RectangleSeed:
    """A seed that creates a rectangle in the Patches game."""

    def __init__(self,
            square:tuple[int, int],
            area:int|None = None,
            shape:str|None=RectangleShape.ANY,
            color:str|None="#FFFFFF"
        ) -> object:
        """
        Args:
            square: The board position of the seed as a `(row, column)` tuple.
            area: The required area of the rectangle to be built.
            shape: The rectagangle's required shape.
            color: The seed's color name or its hex code as a `#RRGGBB` string.
        """
        self.__set_square(square)
        self.__set_shape(shape)
        self.__set_area(area)
        self.__color = Color(color)
        self.__rectangle: Rectangle


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
            if self.shape != RectangleShape.ANY else ""}rectangle"
            f" with{f" a required area of {self.area} squares"
            if self.area is not None else "out any required area"}."
        )


    def __hash__(self) -> int:
        return hash((self.color_code, self.square, self.shape, self.area))


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
            and self.shape == other.shape
        )


    def __ne__(self, other:object) -> bool:
        return not self.__eq__(other)


    @staticmethod
    def __is_perfect_square(n:int) -> bool:
        """
        Check if a number is a perfect square.
        
        Args:
            n: The number to check.

        Returns:
            `True` if `n` is a perfect square, `False` otherwise.
        """
        return sqrt(n) % 1 == 0


    def to_dict(self) -> dict[str, Any]:
        return {
            "color": self.color,
            "color_code": self.color_code,
            "square": self.square,
            "shape": self.shape,
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
    def shape(self) -> str:
        """
        The rectangle's required shape.

        Returns:
            The rectangle shape's name required by the seed square.
        """
        return str(self.__shape)

    def __set_shape(self, value:str|None) -> None:

        if value is None:
            self.__shape = RectangleShape.ANY
            return
        
        if not isinstance(value, str):
            msg = f"The rectangle shape must be a string. Got a {type(value).__name__} instead."
            raise TypeError(msg)
        
        try:
            self.__shape = RectangleShape(value.strip().lower())
        except ValueError as exc:
            valid_shapes = f"'{"', '".join(str(shape) for shape in RectangleShape)}'"
            msg = f"'{value}' is not a valid rectangle shape. Please, input one of theses shapes: {valid_shapes}"
            raise ValueError(msg) from exc


    @property
    def area(self) -> int | None:
        """
        The required rectangle's area.
        
        Returns:
            The rectangle's area required by the seed or `None` if the seed doesn't claim it.
        """
        return self.__area

    def __set_area(self, value: int | None) -> None:

        if value is None:
            self.__area = None
            return

        if not isinstance(value, int):
            msg = f"The required area must be an integer or None. Got {type(value).__name__} instead."
            raise TypeError(msg)

        if value < 1:
            msg = f"The required area must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)

        if self.shape == RectangleShape.SQUARE and not RectangleSeed.__is_perfect_square(value):
            msg = f"The required area ({value!r}) is not a perfect square."
            raise ValueError(msg)

        self.__area = value


    @property
    def color(self) -> str:
        """
        The name of the rectangle seed's color.

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
        The code of rectangle seed's color.

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
        The seed's rectangle.
        
        Returns:
            The rectangle created by the seed square after solving Patches game.
        """
        return self.__rectangle

    @rectangle.setter
    def rectangle(self, value: dict[str, int]) -> None:

        rectangle_area =  value["height"] * value["width"]
        if self.area is not None and rectangle_area != self.area:
            msg = f"The rectangle's area ({rectangle_area}) doesn't attend to the required area ({self.area})."
            raise ValueError(msg)
        
        match self.shape:
            case RectangleShape.VERTICAL:
                if value["height"] <= value["width"]:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f" Its height ({value["height"]!r}) should be greater than its width ({value["width"]!r})."
                    )
                    raise ValueError(msg)
            
            case RectangleShape.HORIZONTAL:
                if value["height"] >= value["width"]:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f" Its width ({value["width"]!r}) should be greater than its height ({value["height"]!r})."
                    )
                    raise ValueError(msg)
            
            case RectangleShape.SQUARE:
                if value["height"] != value["width"]:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f" Its height ({value["height"]!r}) should be equal to its width ({value["width"]!r})."
                    )
                    raise ValueError(msg)

        self.__rectangle = Rectangle(
            top_left=(value["top"], value["left"]),
            dims=(value["height"], value["width"])
        )
