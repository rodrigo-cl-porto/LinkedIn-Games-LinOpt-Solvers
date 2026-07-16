from math import sqrt

from ..color_mixin import ColorMixin
from .rectangle import Rectangle
from .rectangle_shape import RectangleShape


class SeedSquare(ColorMixin):
    """A seed square that creates a rectangle in the Patches game"""

    def __init__(self, 
        square:tuple[int, int],
        area:int|None=None,
        shape:RectangleShape=RectangleShape.ANY,
        color:str|None=None,
        color_code:str|None=None
    ) -> None:
        super().__init__(color=color, color_code=color_code)
        self.square = square
        self.shape = shape
        self.area = area
        self.__rectangle: Rectangle | None = None


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"square={self.square},\n\t"
            f"shape={type(self.shape).__name__}.{self.shape},\n\t"
            f"area={self.area},\n\t"
            f"color={self.color}\n)"
        )


    def __str__(self) -> str:
        return (
            f"A Patches seed square located at {self.square}"
            f" that creates a {self.color_name} {self.shape.lower() + " " if self.shape != RectangleShape.ANY else ""}rectangle"
            f" with{f" a required area of {self.area} squares" if self.area is not None else "out any required area"}."
        )


    def __hash__(self) -> int:
        return hash((self.square, self.shape, self.area, self.color))


    def __len__(self) -> int:
        return 1
    
    
    def __abs__(self) -> int:
        return 1


    def __eq__(self, other):

        if not isinstance(other, SeedSquare):
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
    def shape(self) -> str:
        """Required shape of the seed square as a RectangleShape enum."""
        return str(self._shape)

    @shape.setter
    def shape(self, value:RectangleShape=RectangleShape.ANY) -> None:

        if not isinstance(value, RectangleShape):
            msg = f"The rectangle type must be a RectangleShape class. Got a {type(value).__name__} type instead."
            raise TypeError(msg)
        
        self._shape = value


    @property
    def area(self) -> int | None:
        """Required rea of the seed square as a positive integer or None."""
        return self._area

    @area.setter
    def area(self, value: int | None) -> None:
        
        if value is not None and not isinstance(value, int):
            msg = f"The required area must be an integer or None. Got {type(value).__name__} instead."
            raise TypeError(msg)

        if value is not None:
            if value < 1:
                msg = f"The required area must be a positive integer. Got {value!r} instead."
                raise ValueError(msg)

            if self.shape == RectangleShape.SQUARE and not SeedSquare.__is_perfect_square(value):
                msg = f"The required area ({value!r}) is not a perfect square."
                raise ValueError(msg)

        self._area = value


    @property
    def rectangle(self) -> Rectangle:
        """Rectangle object created by the seed square."""
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
