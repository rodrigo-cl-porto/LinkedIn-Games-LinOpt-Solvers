from enum import StrEnum
from math import sqrt
from matplotlib.colors import CSS4_COLORS
import re


class RecType(StrEnum):
    ANY = "Any"
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"
    SQUARE = "Square"


class TipSeed:

    def __init__(self, color:str, seed_square:tuple[int, int], rect_type:RecType, seed_area:int|None) -> None:
        self.color = color
        self.seed_square = seed_square
        self.rect_type = rect_type
        self.seed_area = seed_area


    def __repr__(self) -> str:
        return (
            "TipSeed(\n\t"
            f"color={self.color},\n\t"
            f"seed_square={self.seed_square},\n\t"
            f"rect_type={self.rect_type},\n\t"
            f"seed_area={self.seed_area}\n)"
        )


    def __str__(self) -> str:
        return (
            "TipSeed("
            f"seed_square={self.seed_square}, "
            f"rect_type={self.rect_type}, "
            f"seed_area={self.seed_area} "
            f"color={self.color})"
        )
    

    def __hash__(self) -> int:
        return hash((self._seed_square, self._rect_type, self._seed_area, self._color))
    

    def __len__(self) -> int:
        if self._seed_area:
            return self._seed_area
        else:
            return 0
    

    @staticmethod
    def __is_perfect_square(n:int) -> bool:
        return sqrt(n) % 1 == 0


    @property
    def color(self) -> str:
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
    def seed_square(self) -> tuple[int, int]:
        return self._seed_square

    @seed_square.setter
    def seed_square(self, value: tuple[int, int]) -> None:

        if not isinstance(value, tuple):
            msg = f"Seed square must be a tuple. Got a {type(value)} type instead."
            raise ValueError(msg)
        
        if len(value) != 2:
            msg = f"Seed square must be a pair (m,n). Got a tuple with length {len(value)}."
            raise ValueError(msg)
        
        if any(not isinstance(coord, int) or isinstance(coord, bool) or coord < 1 for coord in value):
            msg = f"Seed square coordinates must be positive integers. Got {value!r} instead."
            raise ValueError(msg)
        
        self._seed_square = value


    @property
    def rect_type(self) -> RecType:
        return self._rect_type

    @rect_type.setter
    def rect_type(self, value:RecType=RecType.ANY) -> None:

        if not isinstance(value, RecType):
            msg = f"The rectangle type must be a RecType class. Got a {type(value)} type instead."
            raise TypeError(msg)
        
        self._rect_type = value


    @property
    def seed_area(self) -> int | None:
        return self._seed_area

    @seed_area.setter
    def seed_area(self, value: int | None) -> None:
        # Allow None or a positive integer
        if value is not None and not isinstance(value, int):
            msg = f"The tip area must be an integer or None. Got {type(value)} instead."
            raise TypeError(msg)

        if value is not None:
            if value < 1:
                msg = f"The tip area must be a positive integer. Got {value!r} instead."
                raise ValueError(msg)

            if self.rect_type == RecType.SQUARE and not TipSeed.__is_perfect_square(value):
                msg = f"The tip area ({value!r}) is not a perfect square."
                raise ValueError(msg)

        self._seed_area = value


class Rectangle(TipSeed):

    def __init__(self, color:str, seed_square:tuple[int, int], rect_type:RecType, seed_area:int|None, x:int, y:int, width:int, height:int) -> None:
        super().__init__(color, seed_square, rect_type, seed_area)
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def __repr__(self) -> str:
        return (
            "Rectangle(\n\t"
            f"color={self._color},\n\t"
            f"seed_square={self.seed_square},\n\t"
            f"rect_type={self.rect_type},\n\t"
            f"seed_area={self.seed_area},\n\t"
            f"x={self.x},\n\t"
            f"y={self.y},\n\t"
            f"width={self.width},\n\t"
            f"height={self.height}\n)"
        )


    def __str__(self) -> str:
        return (
            "Rectangle("
            f"color={self._color}, "
            f"x={self._x}, "
            f"y={self._y}, "
            f"width={self._width}, "
            f"height={self._height}, "
            f"squares={self.squares})"
        )


    def __hash__(self) -> int:
        return hash((
            self._color,
            self._seed_square,
            self._rect_type,
            self._seed_area,
            self._x,
            self._y,
            self._width,
            self._height
        ))


    def __len__(self) -> int:
        return self._width * self._height
    

    def __eq__(self, other) -> bool:

        if not isinstance(other, Rectangle):
            return False
        
        return (
            self.color == other.color and
            self.seed_area == other.self.seed_area and
            self.rect_type == other.rect_type and
            self.seed_area == other.seed_area and
            self.x == other.x and
            self.y == other.y and
            self.width == other.width and
            self.height == other.height
        )


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The x position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The x position must be positive. Got {value!r} instead."
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
            msg = f"The y position must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        self._y = value


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
        
        if not hasattr(self, "_height"):
            self._width = value
            return None
        
        if self.height is None:
            self._width = value
            return None

        if self.height * value != self.seed_area:
            msg = f"The width ({value!r}) and height ({self.height!r}) do not match the tip area ({self.seed_area!r})."
            raise ValueError(msg)
        
        match self.rect_type:
            case RecType.VERTICAL:
                if value >= self.height:
                    msg = f"The width ({value!r}) cannot be greater or equal of the height ({self.height!r}) in a Vertical Rectangle."
                    raise ValueError(msg)

            case RecType.HORIZONTAL:
                if value <= self.height:
                    msg = f"The width ({value!r}) cannot be less or equal of the height ({self.height!r}) in a Horizontal Rectangle."
                    raise ValueError(msg)
            
            case RecType.SQUARE:
                if value != self.height:
                    msg = f"The width ({value!r}) cannot differ from the height ({self.height!r}) in a Square Rectangle."
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
            msg = f"The height must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        if not hasattr(self, "_width"):
            self._height = value
            return None

        if self.width is not None:
            self._height = value
            return None

        if self.width * value != self.seed_area:
            msg = f"The width ({self.width!r}) and height ({value!r}) do not match the tip area ({self.seed_area!r})."
            raise ValueError(msg)
        
        match self._rect_type:
            case RecType.VERTICAL:
                if value <= self.width:
                    msg = f"The height ({value!r}) cannot be less or equal of the width ({self.width!r}) in a Vertical Rectangle."
                    raise ValueError(msg)

            case RecType.HORIZONTAL:
                if value >= self.width:
                    msg = f"The height ({value!r}) cannot be greater or equal of the width ({self.width!r}) in a Horizontal Rectangle."
                    raise ValueError(msg)
            
            case RecType.SQUARE:
                if value != self.width:
                    msg = f"The height ({value!r}) cannot differ from the width ({self.width!r}) in a Square Rectangle."
                    raise ValueError(msg)
        
        self._height = value


    @property
    def squares(self) -> tuple[tuple[int, int], ...]:
        """Squares covered by the rectangle (row,col) tuples"""

        if self.x < 1 or self.y < 1 or self.width < 1 or self.height < 1:
            return ()
        
        return tuple((i, j) for i in range(self.y, self.y + self.height) for j in range(self.x, self.x + self.width))
