from enum import StrEnum
from math import sqrt
from matplotlib.colors import CSS4_COLORS
import re

from .rectangle import Rectangle


class RectangleShape(StrEnum):
    """Type of rectangle shape for a RectangleSeed."""

    ANY = "ANY"
    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"
    SQUARE = "SQUARE"


class RectangleSeed:
    """A seed for a rectangle in the Patches game, defined by its color, square position, shape, and area."""

    def __init__(
            self,
            color:str,
            square:tuple[int, int],
            shape:RectangleShape,
            area:int | None
        ) -> None:
        self.color = color
        self.square = square
        self.shape = shape
        self.area = area
        self.__rectangle = None


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"color={self.color},\n\t"
            f"square={self.square},\n\t"
            f"shape={type(self.shape).__name__}.{self.shape},\n\t"
            f"area={self.area}\n)"
        )


    def __str__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"square={self.square}, "
            f"shape={type(self.shape).__name__}.{self.shape}, "
            f"area={self.area} "
            f"color={self.color})"
        )


    def __hash__(self) -> int:
        return hash((self.color, self.square, self.shape, self.area,))


    def __len__(self) -> int:
        return 1
    
    
    def __abs__(self) -> int:
        return 1


    def __eq__(self, other):

        if not isinstance(other, RectangleSeed):
            return False
        
        return (
            self.square == other.square
            and self.area == other.area
            and self.shape == other.shape
        )


    def __ne__(self, other):
        return not self.__eq__(other)


    @staticmethod
    def __is_perfect_square(n:int) -> bool:
        return sqrt(n) % 1 == 0


    @property
    def color(self) -> str:
        """Color of the rectangle seed as a hexcode string (#RRGGBB)."""
        return self._color

    @color.setter
    def color(self, value:str="#FFFFFF") -> None:

        try:
            hex_code = CSS4_COLORS[value.strip().lower()]

        except KeyError:
            pattern = re.compile(r"^\#[0-9A-F]{6}$", re.IGNORECASE)

            if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
                msg = f"The color must be a color name or a hex code like '#RRGGBB'. Got {value!r} instead."
                raise ValueError(msg)
            
            self._color = value

        else:
            self._color = hex_code


    @property
    def square(self) -> tuple[int, int]:
        """Position of the rectangle seed on the Zip board as a tuple (row, column)."""
        return self._square

    @square.setter
    def square(self, value: tuple[int, int]) -> None:

        if not isinstance(value, tuple):
            msg = f"Seed square must be a tuple. Got a {type(value).__name__} type instead."
            raise ValueError(msg)
        
        if len(value) != 2:
            msg = f"Seed square must be a pair (m,n). Got a tuple with length {len(value)}."
            raise ValueError(msg)
        
        if any(not isinstance(coord, int) or isinstance(coord, bool) or coord < 1 for coord in value):
            msg = f"Seed square coordinates must be positive integers. Got {value!r} instead."
            raise ValueError(msg)
        
        self._square = value


    @property
    def shape(self) -> RectangleShape:
        """Required shape of the rectangle seed as a RectangleShape enum."""
        return self._shape

    @shape.setter
    def shape(self, value:RectangleShape = RectangleShape.ANY) -> None:

        if not isinstance(value, RectangleShape):
            msg = f"The rectangle type must be a RectangleShape class. Got a {type(value).__name__} type instead."
            raise TypeError(msg)
        
        self._shape = value


    @property
    def area(self) -> int | None:
        """Required rea of the rectangle seed as a positive integer or None."""
        return self._area

    @area.setter
    def area(self, value: int | None) -> None:
        
        if value is not None and not isinstance(value, int):
            msg = f"The tip area must be an integer or None. Got {type(value).__name__} instead."
            raise TypeError(msg)

        if value is not None:
            if value < 1:
                msg = f"The tip area must be a positive integer. Got {value!r} instead."
                raise ValueError(msg)

            if self.shape == RectangleShape.SQUARE and not RectangleSeed.__is_perfect_square(value):
                msg = f"The tip area ({value!r}) is not a perfect square."
                raise ValueError(msg)

        self._area = value


    @property
    def rectangle(self) -> Rectangle:
        """Rectangle object created by the rectangle seed."""
        return self.__rectangle

    def _set_rectangle(self, value:Rectangle) -> None:
        """Set the rectangle object created by the rectangle seed."""

        if self.area is not None:
            if len(value) != self.area:
                msg = f"The rectangle's area ({len(value)}) doesn't attend to the required area ({self.area})."
                raise ValueError(msg)

        match self.shape:
            
            case RectangleShape.VERTICAL:
                if value.height <= value.width:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f"Its height ({value.height!r}) should be greater than its width ({value.width!r})."
                    )
                    raise ValueError(msg)

            case RectangleShape.HORIZONTAL:
                if value.height >= value.width:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f"Its width ({value.width!r}) should be greater than its height ({value.height!r})."
                    )
                    raise ValueError(msg)
            
            case RectangleShape.SQUARE:
                if value.height != value.width:
                    msg = (
                        f"The rectangle doesn't have {self.shape.lower} shape."
                        f"Its height ({value.height!r}) should be equal to its width ({value.width!r})."
                    )
                    raise ValueError(msg)

        self.__rectangle = value
