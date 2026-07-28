from math import sqrt
from typing import Self

from ..core._color import Color
from ._rectangle import Rectangle
from ._rectangle_shape import RectangleShape


class SeedSquare:
    """A seed square that creates a rectangle in the Patches game

    Attributes:
        square (tuple[int, int]): The position of the rectangle seed on the Zip board.
        shape (str): The required shape of the seed square.
        area (int|None): The required area of the seed square.
        color (str): The color of the rectangle created by the seed.
        color_code (str): The hexadecimal color code of the rectangle created by the seed.
        rectangle (Rectangle): The rectangle object created by the seed.
    """
    def __init__(self, square:tuple[int, int], area:int|None=None, shape:str="any", color:str="white") -> None:
        """
        Args:
            square (tuple[int, int]): The position of the seed on the Zip board.
            area (int | None): The required area of the seed square.
            shape (str): The required shape of the seed square.
            color (str): The color of the seed square.
        """
        self.__set_square(square)
        self.__set_shape(shape)
        self.__set_area(area)
        self.__color = Color(color)
        self.__rectangle: Rectangle | None = None


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
        return hash((self.square, self.shape, self.area, self.color_code))


    def __len__(self) -> int:
        return 1


    def __abs__(self) -> int:
        return 1


    def __eq__(self, other:Self) -> bool:
        if not isinstance(other, SeedSquare):
            return False
        return (self.square == other.square and self.area == other.area and self.shape == other.shape)


    def __ne__(self, other:Self) -> bool:
        return not self.__eq__(other)


    @staticmethod
    def __is_perfect_square(n:int) -> bool:
        """Check if a number is a perfect square.
        
        Args:
            n (int): The number to check.

        Returns:
            bool: True if `n` is a perfect square, False otherwise.
        """
        return sqrt(n) % 1 == 0


    @property
    def square(self) -> tuple[int, int]:
        """tuple[int, int]: Position of the rectangle seed on the Zip board as a tuple (row, column)."""
        return self.__square

    def __set_square(self, value: tuple[int, int]) -> None:

        if not isinstance(value, tuple):
            msg = f"Seed square must be a tuple. Got a {type(value).__name__} type instead."
            raise TypeError(msg)
        
        if len(value) != 2:
            msg = (
                "Seed square must be a pair (m,n)."
                f" Got a tuple with length {len(value)}."
            )
            raise ValueError(msg)
        
        if (
            any(not isinstance(coord, int)
            or isinstance(coord, bool)
            or coord < 1 for coord in value)
        ):
            msg = f"Seed square coordinates must be positive integers. Got {value!r} instead."
            raise ValueError(msg)
        
        self.__square = value


    @property
    def shape(self) -> str:
        """The rectangle shape required by the seed square."""
        return str(self.__shape)

    def __set_shape(self, value:str) -> None:

        if value is None:
            self.__shape = RectangleShape("any")
            return

        if not isinstance(value, str):
            msg = f"The rectangle shape must be a string. Got a {type(value).__name__} instead."
            raise TypeError(msg)

        try:
            self.__shape = RectangleShape(value.strip().lower())
        except ValueError as exc:
            valid__shapes = f"'{"', '".join(str(shape) for shape in RectangleShape)}'"
            msg = f"'{value}' is not a valid rectangle shape. Please, input one of theses shapes: {valid__shapes}"
            raise ValueError(msg) from exc


    @property
    def area(self) -> int | None:
        """Required rea of the seed square as a positive integer or None."""
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

        if self.shape == RectangleShape.SQUARE and not SeedSquare.__is_perfect_square(value):
            msg = f"The required area ({value!r}) is not a perfect square."
            raise ValueError(msg)

        self.__area = value


    @property
    def color(self) -> str:
        """The color name of the seed square."""
        return self.__color.name
    
    @color.setter
    def color(self, value:str) -> None:
        self.__color.color = value


    @property
    def color_code(self) -> str:
        """The hexadecimal color code of the seed square."""
        return self.__color.hex
    
    @color_code.setter
    def color_code(self, value:str) -> None:
        self.__color.hex = value


    @property
    def rectangle(self) -> Rectangle:
        """The rectangle created by the seed square."""
        return self.__rectangle

    def _set_rectangle(self, value:Rectangle) -> None:
        """Set the rectangle object created by the rectangle seed."""
        if self.area is not None:
            if value.area != self.area:
                msg = f"The rectangle's area ({value.area}) doesn't attend to the required area ({self.area})."
                raise ValueError(msg)

        match self.shape:
            
            case RectangleShape.VERTICAL:
                if value.height <= value.width:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f" Its height ({value.height!r}) should be greater than its width ({value.width!r})."
                    )
                    raise ValueError(msg)
            
            case RectangleShape.HORIZONTAL:
                if value.height >= value.width:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f" Its width ({value.width!r}) should be greater than its height ({value.height!r})."
                    )
                    raise ValueError(msg)
            
            case RectangleShape.SQUARE:
                if value.height != value.width:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f" Its height ({value.height!r}) should be equal to its width ({value.width!r})."
                    )
                    raise ValueError(msg)

        self.__rectangle = value
