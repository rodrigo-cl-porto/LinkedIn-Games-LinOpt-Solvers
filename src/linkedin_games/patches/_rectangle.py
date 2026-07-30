from typing import Self

from ..core._color import Color


class Rectangle:
    """A Patches rectangle, used as part of the game's solution."""
    def __init__(self, top_left:tuple[int, int], dims:tuple[int, int], color:str|None=None) -> None:
        """
        Args:
            top_left: Board position of the rectangle's top-left square as `(row, column)`.
            dims: Rectangle dimensions as `(width, height)`.
            color: A color name or a hex code as `#RRGGBB` string.
        """
        self.top_left = top_left
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
            f" with top-left square at ({self.top_left})"
            f" with dimensions of {self.dims}"
        )
    

    def __hash__(self) -> int:
        return hash((self.top, self.left, self.width, self.height, self.color_code))


    def __len__(self) -> int:
        return self.width * self.height


    def __eq__(self, other:Self) -> bool:

        if not isinstance(other, Rectangle):
            return False
        
        return self.top_left == other.top_left and self.dims == other.dims


    def __ne__(self, other:Self) -> bool:
        return not self.__eq__(other)


    def to_dict(self) -> dict[str, str|tuple[int, int]]:
        return {
            "color": self.color,
            "color_code": self.color_code,
            "top_left": (self.top, self.left),
            "dims": (self.width, self.height)
        }


    @property
    def area(self) -> int:
        """
        The rectangle's area.

        Returns:
            Total quantity of squares in the rectangle.
        """
        return len(self)


    @property
    def dims(self) -> tuple[int, int]:
        """
        Dimensions of the rectangle.

        Returns:
            Rectangle dimensions as a `(width, height)` tuple.
        """
        return (self.width, self.height)
    
    @dims.setter
    def dims(self, value:tuple[int, int]) -> None:
        self.width, self.height = value


    @property
    def top_left(self) -> tuple[int, int]:
        """
        Board position of the rectangle's top-left square.

        Returns:
            Rectangle dimensions as a `(row, column)` tuple.
        """
        return (self.top, self.left)
    
    @top_left.setter
    def top_left(self, value:tuple[int, int]) -> None:
        self.top, self.left = value


    @property
    def top(self) -> int:
        """
        The board position of the rectangle's top row.
        
        Returns:
            Index position of the rectangle's first row.
        """
        return self.__top

    @top.setter
    def top(self, value:int) -> None:

        if not isinstance(value, int):
            msg = f"The top row's position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The top row's position must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        self.__top = value


    @property
    def left(self) -> int:
        """
        The board position of the rectangle's leftmost column.
        
        Returns:
            Index position of the rectangle's first column.
        """
        return self.__left

    @left.setter
    def left(self, value:int) -> None:

        if not isinstance(value, int):
            msg = f"The leftmost column's position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The leftmost column's position must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        self.__left = value


    @property
    def width(self) -> int:
        """
        The width of the rectangle.
        
        Returns:
            The rectangle's number of columns.
        """
        return self.__width

    @width.setter
    def width(self, value:int) -> None:

        if not isinstance(value, int):
            msg = f"The width must be an integer. Got {value!r}"
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The width must be a positive integer. Got {value!r} instead."
            raise ValueError(msg)
        
        if not hasattr(self, "__height"):
            self.__width = value
            return
        
        if self.height is None:
            self.__width = value
            return
        
        self.__width = value


    @property
    def height(self) -> int:
        """
        The height of the rectangle.

        Returns:
            The rectangle's number of rows.
        """
        return self.__height

    @height.setter
    def height(self, value:int) -> None:

        if not isinstance(value, int):
            msg = f"The height must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The height must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        if not hasattr(self, "__width"):
            self.__height = value
            return
        
        if self.width is not None:
            self.__height = value
            return
        
        self.__height = value


    @property
    def squares(self) -> tuple[tuple[int, int]]:
        """
        The board squares occupied by the rectangle.
        
        Returns:
            All the squares as a tuple of `(row, column)`.
        """
        return tuple(
            (i, j)
            for i in range(self.top, self.top + self.height)
            for j in range(self.left, self.left + self.width)
        )


    @property
    def color(self) -> str:
        """
        The name of the rectangle's color.

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
        The code of rectangle's color.

        Returns:
            Hex code color as a `"#RRGGBB"` string.
        """
        return self.__color.hex
    
    @color_code.setter
    def color_code(self, value:str) -> None:
        self.__color.hex = value
