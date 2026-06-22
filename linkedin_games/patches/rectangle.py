from enum import StrEnum
from math import sqrt
import re


class RecType(StrEnum):
    ANY = "Any"
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"
    SQUARE = "Square"


class Rectangle:

    def __init__(
        self,
        tip_square: tuple[int, int],
        tip_type: RecType = RecType.ANY,
        tip_area: int | None = None,
        color: str = "#000000",
        width: int = 0,
        height: int = 0,
        x: int = 0,
        y: int = 0,
    ) -> None:
        self._tip_square = tip_square
        self._tip_type = tip_type
        self._tip_area = tip_area
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height


    def __repr__(self) -> str:
        return (
            "Rectangle(\n\t"
            f"tip_square={self.tip_square},\n\t"
            f"tip_type={self.tip_type},\n\t"
            f"tip_area={self.tip_area},\n\t"
            f"x={self.x},\n\t"
            f"y={self.y},\n\t"
            f"width={self.width},\n\t"
            f"height={self.height}\n)"
        )


    def __str__(self) -> str:
        return (
            "Rectangle("
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"squares={self.squares})"
        )


    def __eq__(self, other) -> bool:

        if not isinstance(other, Rectangle):
            return False
        
        return (
            self.x == other.x and 
            self.y == other.y and
            self.width == other.width and
            self.height == other.height
        )
    

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    def __len__(self) -> int:
        return self._width * self._height


    @staticmethod
    def __is_perfect_square(n:int) -> bool:
        return sqrt(n) % 1 == 0


    @property
    def tip_type(self) -> RecType:
        return self._tip_type

    @tip_type.setter
    def tip_type(self, value:RecType=RecType.ANY) -> None:

        if not isinstance(value, RecType):
            msg = f"tip_type must be a RecType. Got {type(value)} instead."
            raise TypeError(msg)
        
        self._tip_type = value


    @property
    def tip_square(self) -> tuple[int, int]:
        return self._tip_square

    @tip_square.setter
    def tip_square(self, value: tuple[int, int]) -> None:

        if not (isinstance(value, tuple) and len(value) == 2 and all(isinstance(v, int) for v in value)):
            msg = f"tip_square must be a tuple of two integers (row, col). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(v < 1 for v in value):
            msg = f"tip_square coordinates must be positive integers. Got {value!r} instead."
            raise ValueError(msg)
        
        self._tip_square = value


    @property
    def tip_area(self) -> int | None:
        return self._tip_area

    @tip_area.setter
    def tip_area(self, value: int) -> None:
        
        if not isinstance(value, int):
            msg = f"tip_area must be an int or None. Got {type(value)} instead"
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The area must be a positive integer. Got {value!r} instead"
            raise ValueError(msg)
        
        if self.tip_type == RecType.SQUARE and not Rectangle.__is_perfect_square(value):
            msg = f"The informed area ({value!r}) is not a perfect square."
            raise ValueError(msg)
        
        self._tip_area = value


    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value:str) -> None:

        pattern = re.compile(r"^\#[0-9A-F]{6}$", re.IGNORECASE)

        if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
            msg = f"The color must be a hex code like '#RRGGBB'. Got {value!r} instead."
            raise ValueError(msg)
        
        self._color = value


    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The width must be an integer. Got {value!r}"
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The width must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)
        
        self._width = value


    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The height must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The height must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)
        
        self._height = value


    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The x position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The x position must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)
        
        self._x = value


    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The y position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The y position must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)
        
        self._y = value


    @property
    def squares(self) -> tuple[tuple[int, int], ...]:
        """Squares covered by the rectangle (row,col) tuples"""

        if self.x < 1 or self.y < 1 or self.width < 1 or self.height < 1:
            return ()
        
        return tuple((i, j) for i in range(self.y, self.y + self.height) for j in range(self.x, self.x + self.width))
