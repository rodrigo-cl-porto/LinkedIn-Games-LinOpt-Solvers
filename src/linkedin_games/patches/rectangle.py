from typing import Self

from ..color import Color


class Rectangle:
    """A Patches rectangle, used as part of the game's solution.
    
    Attributes:
        top_left_square (tuple[int, int]): The position of the rectangle's top-left square.
        dims (tuple[int, int]): The dimensions of the rectangle as (width, height).
        top (int): The position of the rectangle's topmost row.
        left (int): The position of the rectangle's leftmost column.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        color (str|None): The color of the rectangle.
    """

    def __init__(self, top_left_square:tuple[int, int], 
            dims:tuple[int, int], color:str|None=None) -> Self:
        """_summary_

        Args:
            top_left_square (tuple[int, int]): _description_
            dims (tuple[int, int]): _description_
            color (str | None, optional): _description_. Defaults to None.

        Returns:
            Self: _description_
        """
        self.top_left_square = top_left_square
        self.dims = dims
        self.__color = Color(color)


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"left={self.left},\n\t"
            f"top={self.top},\n\t"
            f"width={self.width},\n\t"
            f"height={self.height},\n\t"
            f"color_code={self.color_code}\n)"
        )


    def __str__(self) -> str:
        return (
            f"A {self.color} {type(self).__name__}"
            f" with top-left square at ({self.top_left_square})"
            f" with dimensions of {self.dims}"
        )


    def __hash__(self) -> int:
        return hash((
            self.top,
            self.left,
            self.width,
            self.height,
            self.color_code
        ))


    def __len__(self) -> int:
        return self.width * self.height


    def __eq__(self, other:Self) -> bool:

        if not isinstance(other, Rectangle):
            return False
        
        return (
            self.left == other.left
            and self.top == other.top
            and self.width == other.width
            and self.height == other.height
        )


    def __ne__(self, other:Self) -> bool:
        return not self.__eq__(other)


    @property
    def dims(self) -> tuple[int, int]:
        return (self._width, self._height)
    
    @dims.setter
    def dims(self, value:tuple[int, int]) -> None:
        self.width = value[0]
        self.height = value[1]


    @property
    def top_left_square(self) -> tuple[int, int]:
        return (self._top, self._left)
    
    @top_left_square.setter
    def top_left_square(self, value:tuple[int, int]) -> None:
        self.top = value[0]
        self.left = value[1]


    @property
    def top(self) -> int:
        """The position of the rectangle's topmost row."""
        return self._top

    @top.setter
    def top(self, value:int) -> None:
        if not isinstance(value, int):
            msg = f"The top row's position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The top row's position must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        self._top = value


    @property
    def left(self) -> int:
        """The position of the rectangle's leftmost column."""
        return self._left

    @left.setter
    def left(self, value:int) -> None:

        if not isinstance(value, int):
            msg = (
                "The leftmost column's position must be an integer."
                f" Got {value!r} instead."
            )
            raise TypeError(msg)
        
        if value < 1:
            msg = (
                "The leftmost column's position must be positive."
                f" Got {value!r} instead."
            )
            raise ValueError(msg)
        
        self._left = value


    @property
    def width(self) -> int:
        """The width of the rectangle."""
        return self._width

    @width.setter
    def width(self, value:int) -> None:

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
        
        self._width = value


    @property
    def height(self) -> int:
        """The height of the rectangle."""
        return self._height

    @height.setter
    def height(self, value:int) -> None:

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
        
        self._height = value


    @property
    def squares(self) -> tuple[tuple[int, int]]:
        """The squares occupied by the rectangle."""
        return tuple(
            (i, j)
            for i in range(self.top, self.top + self.height)
            for j in range(self.left, self.left + self.width)
        )


    @property
    def color(self) -> str:
        return self.__color.name
    
    @color.setter
    def color(self, value:str) -> None:
        self.__color.color = value


    @property
    def color_code(self) -> str:
        return self.__color.hex
    
    @color_code.setter
    def color_code(self, value:str) -> None:
        self.__color.hex = value
