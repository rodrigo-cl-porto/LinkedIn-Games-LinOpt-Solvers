from matplotlib.colors import CSS4_COLORS
import re

class Region():

    """
    A class representing a colored region on a Queens board game.

    Attributes:
        squares (set[tuple[int, int]]): A set of tuples representing the coordinates of the squares in the region.
        color (str): The color of the region in hex format (e.g., "#RRGGBB").
    """

    def __init__(self, squares:set[tuple[int, int]], color:str="#FFFFFF"):
        self.squares = squares
        self.color = color


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
        return self._color
    
    @color.setter
    def color(self, value:str) -> None:

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


if __name__ == "__main__":

    # Example usage
    region1 = Region(color="Red", squares={(1, 1), (1, 2)})
    region2 = Region(color="Green", squares={(2, 1), (2, 2)})

    print(region1)
    print(region2)
