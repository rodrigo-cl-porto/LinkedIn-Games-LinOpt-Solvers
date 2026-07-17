from ..color import Color


class Region:
    """A class representing a colored region on a Queens board game."""

    def __init__(self, squares:set[tuple[int, int]], color:str|None=None):
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


    def __eq__(self, other) -> bool:
        if not isinstance(other, Region):
            return False
        
        return self.squares == other.squares


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    def __hash__(self) -> int:
        return hash((frozenset(self.squares), self.color_code))


    @property
    def squares(self) -> set[tuple[int, int]]:
        """Squares in the region."""
        return self._squares

    @squares.setter
    def squares(self, value: set[tuple[int, int]]):

        if not isinstance(value, set):
            msg = f"Squares must be a set. Got {value!r} instead."
            raise TypeError(msg)
        
        if len(value) < 1:
            msg = f"The set of squares must contain at least one square. Got {value!r} instead."
            raise ValueError(msg)
        
        invalid_squares = {square for square in value if not isinstance(square, tuple) or len(square) != 2}
        if invalid_squares:
            msg = f"Each square must be a tuple of length 2. Got the following set of invalid squares: {invalid_squares!r}."
            raise ValueError(msg)
        
        invalid_squares = {square for square in value if any(not isinstance(coord, int) or coord < 1 for coord in square)}
        if invalid_squares:
            msg = f"Each coordinate in the squares must be an positive integer. Got the following set of invalid squares: {invalid_squares!r}."
            raise ValueError(msg)

        self._squares = value


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
