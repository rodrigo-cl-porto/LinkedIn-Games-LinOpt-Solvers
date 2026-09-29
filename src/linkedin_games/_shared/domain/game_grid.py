from abc import ABC, abstractmethod

from ..optimization.solutions._solution import GameSolution


class GameGrid(ABC):
    """An Abstract Base Class for any LinkedIn game grid."""

    def __init__(self, grid_dims: tuple[int, int]) -> None:
        """
        Args:
            `grid_dims`: Grid dimensions as a `(rows, columns)` tuple.
        
        Raises:
            `TypeError`: If `grid_dims` is not a tuple of two integers.
            `ValueError`: If `grid_dims` is not a tuple of two positive integers
                or if the grid's area is smaller than 2 squares.
        """
        self._set_grid_dims(grid_dims)
        self._solution: GameSolution | None = None


    def __len__(self) -> int:
        return self.area


    def __abs__(self) -> int:
        return self.area


    @property
    def area(self) -> int:
        m, n = self._grid_dims
        return m * n


    @property
    def grid_squares(self) -> dict[tuple[int, int], int | str | None]:
        return {(i, j): None for i in range(1, self._height+1) for j in range(1, self._width+1)}


    @property
    def grid_dims(self) -> tuple[int, int]:
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


    @abstractmethod
    def set_solution(self, value: GameSolution) -> None:
        ...


    @property
    def is_solved(self) -> bool:
        return self._solution is not None
