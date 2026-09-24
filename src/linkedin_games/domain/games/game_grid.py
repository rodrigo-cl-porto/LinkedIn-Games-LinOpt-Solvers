from ...optimization.solutions._solution import GameSolution


class GameGrid:
    """An Abstract Base Class for any LinkedIn game grid."""

    def __init__(self, grid_dims:tuple[int, int]) -> None:
        """
        Args:
            `grid_dims`: Grid dimensions as a `(rows, columns)` tuple.
        
        Raises:
            `TypeError`: If `grid_dims` is not a tuple of two integers.
            `ValueError`: If `grid_dims` is not a tuple of two positive integers
                or if the grid's area is smaller than 2 squares.
        """
        self._set_grid_dims(grid_dims)
        self._solution = None


    def __len__(self) -> int:
        m, n = self._grid_dims
        return m * n


    def __abs__(self) -> int:
        return len(self)


    @property
    def area(self) -> int:
        """
        The game grid's area

        Returns:
            The total number of squares on the grid.
        """
        return len(self)


    @property
    def grid_squares(self) -> dict[tuple[int, int], int | None]:
        """
        All the grid squares and their respective assigned values (if any).
        
        Returns:
            Grid squares as a dictionary of `(row, column): value` items.
        """
        if not self._solution:
            return {(i, j): None for i in range(1, self._height) for j in range(1, self._width+1)}

        return self._solution.get("grid_squares")


    @property
    def grid_dims(self) -> tuple[int, int]:
        """
        The grid dimensions.
        
        Returns:
            Dimensions of the grid as a `(rows, columns)` tuple.
        """
        return self._grid_dims


    def _set_grid_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        if len(value) != 2:
            msg = f"Grid dimensions must be a pair (m,n). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(not isinstance(dim, int) or isinstance(dim, bool) for dim in value):
            msg = f"Grid dimensions must be integers. Got {value!r} instead."
            raise TypeError(msg)
        
        if any(dim < 1 for dim in value):
            msg = f"Grid dimensions must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        m, n = value
        if m * n < 2:
            msg = f"The grid is too small for the game. Got grid dimensions of {value!r}."
            raise ValueError(msg)
        
        self._grid_dims = tuple(value)
        self._height = value[0]
        self._width = value[1]


    @property
    def height(self) -> int:
        return self._height


    @property
    def width(self) -> int:
        return self._width


    @property
    def solution(self) -> GameSolution | None:
        return self._solution


    @solution.setter
    def solution(self, value: GameSolution) -> None:
        self._solution = value
