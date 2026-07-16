from ..color_mixin import ColorMixin


class Region(ColorMixin):
    """A class representing a colored region on a Queens board game."""

    def __init__(self, squares:set[tuple[int, int]], color:str|None=None, color_code:str|None = None):
        super().__init__(color=color, color_code=color_code)
        self.squares = squares


    def __repr__(self) -> str:
        return (
            "Region(\n\t"
            f"color={self._color},\n\t"
            f"squares={self._squares!r}\n)"
        )


    def __str__(self) -> str:
        return f"Region with color {self._color} and squares {self._squares!r}."
    

    def __len__(self) -> int:
        return len(self._squares)


    def __eq__(self, other) -> bool:
        if not isinstance(other, Region):
            return False
        
        return self._squares == other.squares and self._color == other.color


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    def __hash__(self) -> int:
        return hash((frozenset(self._squares), self._color))
    

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
