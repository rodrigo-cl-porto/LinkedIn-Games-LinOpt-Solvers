from ..._game_grid import GameGrid
from ...utils.taxicab_distance import TaxicabDistance


class Tango(GameGrid):
    """
    The [LinkedIn Tango](https://www.linkedin.com/games/tango/) game.
    
    A 6x6 game grid with some squares already filled by moons and suns, and which
    can have some pairs of squares with an equal sign or cross sign in-between.
    
    Objective:
        To fill all the squares on the grid with moons 🌙 and suns ☀️.
    
    Rules:
        - The number of moons and suns in each row and column must be the same;
        - There cannot be more than 2 moons or 2 suns in a row, either in a row or column;
        - Squares separated by the `=` sign must contain the same symbol;
        - Squares separated by the `×` sign must contain opposite symbols.
    """
    def __init__(self,
            filled_squares: dict[tuple[int, int], int],
            matching_pairs:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None = None,
            opposite_pairs:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None = None,
        ) -> None:
        """
        Args:
            filled_squares: Starting filled squares as a dictionary of `(row, column): 0 | 1` items.
            matching_pairs: Pairs of matching squares (separated by a `=` sign)
                as a set of `((row1, column1), (row2, column2))`.
            opposite_pairs: Pairs of opposite squares (separated by a `×` sign)
                as a set of `((row1, column1), (row2, column2))`.

        Raises:
            TypeError: If the types of the arguments don't match their required types.
            ValueError: If the quantity of numbered squares exceeds the total number of squares on the grid,
                or if the number of walls exceeds the total number of edges on the grid,
                or if any pair of squares in walls are not adjacent.
        """
        super().__init__(grid_dims=(6,6))
        self.__set_filled_squares(filled_squares)
        self.__set_matching_pairs(matching_pairs)
        self.__set_opposite_pairs(opposite_pairs)


    def __hash__(self) -> int:
        return hash((self._grid_dims, self.__matching_pairs, self.__opposite_pairs, self.__filled_squares))


    @property
    def filled_squares(self) -> dict[tuple[int, int], int]:
        """
        Squares that are already filled with a symbol.
        
        Returns:
            Starting filled squares as a dictionary of `(row, column): 0 | 1` items.
        """
        return self.__filled_squares


    def __set_filled_squares(self, values: dict[tuple[int, int], int]) -> None:
    
        if len(values) > len(self):
            msg = f"The number of filled squares exceeds the amount of grid squares. Got {len(values)} filled squares."
            raise ValueError(msg)

        invalid_items = {square: value for square, value in values.items() if value != 1 and value != 0}
        if invalid_items:
            msg = f"The square values must be of binary type. Invalid values: {invalid_items!r}."
            raise TypeError(msg)

        self.__filled_squares = {square: (1 if value else 0) for square, value in values.items()}


    @property
    def matching_pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        Pairs of matching squares.

        Pairs of squares that are separated by a `=` sign, i.e., that must have the same symbols.

        Returns:
            Pairs of matching squares as a set of `((row1, column1), (row2, column2))`.
        """
        return self.__matching_pairs
    
    
    def __set_matching_pairs(self,
            values:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None
        ) -> None:

        if values is None:
            self.__matching_pairs = None
            return

        invalid_items = [pair for pair in values if not isinstance(pair, tuple) or len(pair) != 2]
        if invalid_items:
            msg = f"matching_pairs must be a collection of pairs of tuples. Invalid pairs: {invalid_items!r}."
            raise TypeError(msg)
        
        invalid_items = [square for pair in values for square in pair if not isinstance(square, tuple)]
        if invalid_items:
            msg = f"Squares in pair must be tuples of positive integers. Invalid squares: {invalid_items!r}."
            raise ValueError(msg)
        
        invalid_items = [
            square for pair in values for square in pair for coord in square
            if not isinstance(coord, int) or coord < 1
        ]
        if invalid_items:
            msg = f"Coordinates must be positive integers. Invalid squares: {invalid_items!r}."
            raise ValueError(msg)

        invalid_items = [pair for pair in values if TaxicabDistance.calculate(*pair) != 1]
        if invalid_items:
            msg = f"Squares in a pair must be consecutive ones. Invalid pairs: {invalid_items!r}."
            raise ValueError(msg)
        
        self.__matching_pairs = list(set(values))


    @property
    def opposite_pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        Pairs of opposite squares.

        Pairs of squares that are separated by a `×` sign, i.e., that must have opposite symbols.

        Returns:
            Pairs of opposite squares as a set of `((row1, column1), (row2, column2))` items.
        """
        return self.__opposite_pairs


    def __set_opposite_pairs(self,
            values: set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None
        ) -> None:

        if values is None:
            self.__opposite_pairs = None
            return

        invalid_items = [pair for pair in values if not isinstance(pair, tuple) or len(pair) != 2]
        if invalid_items:
            msg = f"opposite_pairs must be a collection of pairs of tuples. Invalid pairs: {invalid_items!r}."
            raise TypeError(msg)
        
        invalid_items = [square for pair in values for square in pair if not isinstance(square, tuple)]
        if invalid_items:
            msg = f"Squares in pair must be tuples of positive integers. Invalid squares: {invalid_items!r}."
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in values for square in pair for coord in square
            if not isinstance(coord, int) or coord < 1
        ]
        if invalid_items:
            msg = f"Coordinates must be positive integers. Invalid squares: {invalid_items!r}."
            raise ValueError(msg)

        invalid_items = [pair for pair in values if self._taxicab_distance(*pair) != 1]
        if invalid_items:
            msg = f"Squares in a pair must be consecutive ones. Invalid pairs: {invalid_items!r}."
            raise ValueError(msg)
        
        self.__opposite_pairs = list(set(values))
