from .rec_type import RecType
from .tip_seed import TipSeed


class Rectangle(TipSeed):

    def __init__(self, color:str, seed_square:tuple[int, int], rec_type:RecType, seed_area:int|None, x:int, y:int, width:int, height:int) -> None:
        super().__init__(color, seed_square, rec_type, seed_area)
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f'color="{self.color}",\n\t'
            f"seed_square={self.seed_square},\n\t"
            f"rec_type=RecType.{self.rec_type},\n\t"
            f"seed_area={self.seed_area},\n\t"
            f"x={self.x},\n\t"
            f"y={self.y},\n\t"
            f"width={self.width},\n\t"
            f"height={self.height}\n)"
        )


    def __str__(self) -> str:
        return (
            "Rectangle("
            f"color={self.color}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"squares={self.squares})"
        )


    def __hash__(self) -> int:
        return hash((
            self.color,
            self.seed_square,
            self.rec_type,
            self.seed_area,
            self.x,
            self.y,
            self.width,
            self.height
        ))


    def __len__(self) -> int:
        return self.width * self.height
    

    def __eq__(self, other) -> bool:

        if not isinstance(other, Rectangle):
            return False
        
        return (
            self.color == other.color and
            self.seed_area == other.seed_area and
            self.rec_type == other.rec_type and
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
        
        match self.rec_type:
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
        
        match self._rec_type:
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
    def squares(self) -> tuple[tuple[int, int]]:
        """Squares covered by the rectangle (row,col) tuples"""

        squares = tuple(
            (i, j)
            for i in range(self.y, self.y + self.height)
            for j in range(self.x, self.x + self.width)
        )
        
        return squares
