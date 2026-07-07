class Rectangle:
    """A Zip rectangle defined by its left, top, width, and height."""

    def __init__(self, left:int, top:int, width:int, height:int) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"left={self.left},\n\t"
            f"top={self.top},\n\t"
            f"width={self.width},\n\t"
            f"height={self.height}\n)"
        )


    def __str__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"left={self.left}, "
            f"top={self.top}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"squares={self.squares})"
        )


    def __hash__(self) -> int:
        return hash((
            self.left,
            self.top,
            self.width,
            self.height
        ))


    def __len__(self) -> int:
        return self.width * self.height


    def __eq__(self, other) -> bool:

        if not isinstance(other, Rectangle):
            return False
        
        return (
            self.left == other.left
            and self.top == other.top
            and self.width == other.width
            and self.height == other.height
        )


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    @property
    def left(self) -> int:
        """The position of the rectangle's leftmost column."""
        return self._left

    @left.setter
    def left(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The left position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The left position must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        self._left = value


    @property
    def top(self) -> int:
        """The position of the rectangle's topmost row."""
        return self._top

    @top.setter
    def top(self, value: int) -> None:

        if not isinstance(value, int):
            msg = f"The top position must be an integer. Got {value!r} instead."
            raise TypeError(msg)
        
        if value < 1:
            msg = f"The top position must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        self._top = value


    @property
    def width(self) -> int:
        """The width of the rectangle."""
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
        
        self._width = value


    @property
    def height(self) -> int:
        """The height of the rectangle."""
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
        
        self._height = value


    @property
    def squares(self) -> tuple[tuple[int, int]]:
        """The squares occupied by the rectangle."""

        return tuple(
            (i, j)
            for i in range(self.top, self.top + self.height)
            for j in range(self.left, self.left + self.width)
        )
