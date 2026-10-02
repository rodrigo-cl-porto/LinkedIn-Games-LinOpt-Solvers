from .._shared.domain.game_grid import GameGrid
from .._shared.optimization.solution.solution import GameSolution
from .._shared.utils.taxicab_distance import TaxicabDistance
from ._solution import TangoSolution


class TangoGrid(GameGrid):

    def __init__(self,
            dims: tuple[int, int],
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
        super().__init__(dims)
        self.__set_filled_squares(filled_squares)
        self.__set_matching_pairs(matching_pairs)
        self.__set_opposite_pairs(opposite_pairs)
        self._solution: TangoSolution

    def __hash__(self) -> int:
        return hash((self._dims, self.__matching_pairs, self.__opposite_pairs, self.__filled_squares))

    @property
    def filled_squares(self) -> dict[tuple[int, int], int]:
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
    def matching_pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return self.__matching_pairs
    
    def __set_matching_pairs(self,
            values:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None
        ) -> None:

        if values is None:
            self.__matching_pairs = []
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
    def opposite_pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return self.__opposite_pairs

    def __set_opposite_pairs(self,
            values: set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None
        ) -> None:

        if values is None:
            self.__opposite_pairs = []
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

        invalid_items = [pair for pair in values if TaxicabDistance.calculate(*pair) != 1]
        if invalid_items:
            msg = f"Squares in a pair must be consecutive ones. Invalid pairs: {invalid_items!r}."
            raise ValueError(msg)
        
        self.__opposite_pairs = list(set(values))

    def set_solution(self, value: GameSolution) -> None:
        if not isinstance(value, TangoSolution):
            msg = f"Invalid input. Got a {type(value).__name__} object."
            raise TypeError(msg)
        self._solution = value

    @property
    def squares(self) -> dict[tuple[int, int], int | None]:
        if self._solution:
            return self._solution.squares
        return {
            (i, j): self.filled_squares.get((i, j))
            for i in range(1, self._height+1)
            for j in range(1, self._width+1)
        }

    @property
    def solution(self) -> dict[tuple[int, int], int]:
        return super().solution

    @property
    def moons(self) -> list[tuple[int, int]]:
        if self._solution:
            return self._solution.moons
        return [square for square, value in self.filled_squares.items() if value == 1]

    @property
    def suns(self) -> list[tuple[int, int]]:
        if self._solution:
            return self._solution.suns
        return [square for square, value in self.filled_squares.items() if value == 0]
