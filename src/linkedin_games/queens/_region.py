from ..core._color import Color


class Region:
    """A colored region on a Queens board."""
    
    def __init__(self, squares:set[tuple[int, int]], color:str="white") -> object:
        """
        Args:
            squares: All board squares that make up the region as a set of `(row, column)`.
            color: The region's color's name or its hex code as a `#RRGGBB` string.
        """
        self.squares = squares
        self.__color = Color(color)


    def __repr__(self) -> str:
        return (
            "Region(\n\t"
            f"color_code={self.color_code},\n\t"
            f"squares={self.squares!r}\n)"
        )


    def __str__(self) -> str:
        return f"A {self.color} Queens Region on squares {self.squares!r}."


    def __len__(self) -> int:
        return len(self.squares)


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Region):
            return False
        return self.squares == other.squares


    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


    def __hash__(self) -> int:
        return hash((frozenset(self.squares), self.color_code))


    @property
    def squares(self) -> set[tuple[int, int]]:
        """
        Squares in the region.
        
        Returns:
            All board squares that make up the region as a set of `(row, column)`.
        """
        return self.__squares

    @squares.setter
    def squares(self, value: set[tuple[int, int]]) -> None:

        if not isinstance(value, set):
            msg = f"Squares must be a set. Got {value!r} instead."
            raise TypeError(msg)
        
        if len(value) < 1:
            msg = f"The set of squares cannot be empty. Got {value!r} instead."
            raise ValueError(msg)
        
        invalid_squares = {square for square in value if not isinstance(square, tuple) or len(square) != 2}
        if invalid_squares:
            msg = f"Each square must be a tuple of length 2. Invalid squares: {invalid_squares!r}."
            raise ValueError(msg)
        
        invalid_squares = {
            square for square in value
            if any(not isinstance(coord, int) or coord < 1 for coord in square)
        }
        if invalid_squares:
            msg = f"Each coordinate in the squares must be an positive integer. Invalid squares: {invalid_squares!r}."
            raise ValueError(msg)

        self.__squares = value

    @property
    def color(self) -> str:
        """
        The name of the regions's color.

        Returns:
            The color's name of the region.
        """
        return self.__color.name
    
    @color.setter
    def color(self, value:str) -> None:
        self.__color.color = value

    @property
    def color_code(self) -> str:
        """
        The code of region's color.

        Returns:
            Hex code color as a `"#RRGGBB"` string.
        """
        return self.__color.hex_code
    
    @color_code.setter
    def color_code(self, value:str) -> None:
        self.__color.hex_code = value
