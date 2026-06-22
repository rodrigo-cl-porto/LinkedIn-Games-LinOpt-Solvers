import re

class Region():

    def __init__(self, name:str, squares:set[tuple[int, int]], color:str="#000000"):
        self._name = name
        self._squares = squares
        self._color = color


    def __repr__(self) -> str:
        return f"Region(name={self._name}, color={self._color}, squares={self._squares!r})"


    def __str__(self) -> str:
        return f"Region {self._name} with color {self._color} and squares {self._squares!r}"
    

    def __len__(self) -> int:
        return len(self._squares)


    def __eq__(self, other) -> bool:
        if not isinstance(other, Region):
            return False
        
        return self._squares == other.squares and self._color == other.color


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value:str) -> None:
        self._name = value
    

    @property
    def squares(self) -> set[tuple[int, int]]:
        return self._squares

    @squares.setter
    def squares(self, value:set[tuple[int, int]]):

        if isinstance(value, list):
            self._squares = set(*value)

        self._squares = value


    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value:str):

        pattern = re.compile(r"^\#[0-9A-F]{6}$", re.IGNORECASE)

        if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
            msg = f"The color must be a hex code like '#RRGGBB'. Got {value!r} instead."
            raise ValueError(msg)
        
        self._color = value
