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
    

    @staticmethod
    def __hex_to_rgb(hex_code:str) -> tuple[int, int, int]:
        """Converts '#RRGGBB' to an (R, G, B) tuple."""
        hex_code = hex_code.lstrip('#')
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


    @staticmethod
    def __get_closest_color_name(hex_code:str) -> str:
        """Finds the closest named color by calculating Euclidean distance."""
        target_rgb = Region.__hex_to_rgb(hex_code)
        closest_name = None
        min_distance = float('inf')

        for name, hex_val in CSS4_COLORS.items():
            color_rgb = Region.__hex_to_rgb(hex_val)
            # Calculate 3D Euclidean distance between RGB values
            distance_squared = sum((t - c) ** 2 for t, c in zip(target_rgb, color_rgb))
            
            if distance_squared < min_distance:
                min_distance = distance_squared
                closest_name = name
                
        return closest_name


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
        """Color of the region in hex format (e.g., "#RRGGBB")."""
        return self._color
    
    @color.setter
    def color(self, value:str="#FFFFFF") -> None:

        try:
            color_name = value.strip().lower()
            hex_code = CSS4_COLORS[color_name]

        except KeyError:
            # Informed a hex code"
            pattern = re.compile(r"^\#[0-9A-F]{6}$", re.IGNORECASE)

            if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
                msg = f"The color must be a color name or a hex code like '#RRGGBB'. Got {value!r} instead."
                raise ValueError(msg)
            
            self._color = value
            self.__set_color_name(value)

        else:
            # Informed a valid color name
            self._color_name = color_name
            self._color = hex_code


    @property
    def color_name(self) -> str:
        return self._color_name
    
    def __set_color_name(self, value:str) -> None:
        self._color_name = Region.__get_closest_color_name(value)


    @property
    def square(self) -> tuple[int, int]:
        """Position of the rectangle seed on the Zip board as a tuple (row, column)."""
        return self._square


if __name__ == "__main__":

    # Example usage
    region1 = Region(color="Red", squares={(1, 1), (1, 2)})
    region2 = Region(color="Green", squares={(2, 1), (2, 2)})

    print(region1)
    print(region2)
