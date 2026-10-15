from .._shared.domain.game_grid import GameGrid
from .._shared.optimization.solution.solution import GameSolution
from .._shared.utils.taxicab_distance import TaxicabDistance
from ._solution import ZipSolution


class ZipGrid(GameGrid):

    def __init__(self,
            dims: tuple[int, int],
            numbered_squares: list[tuple[int, int]],
            walls: list[tuple[tuple[int, int], tuple[int, int]]] | None = None
        ) -> None:
        super().__init__(dims)
        self.__set_numbered_squares(numbered_squares)
        self.__set_walls(walls)
        self._solution: ZipSolution

    def __hash__(self) -> int:
        return hash((self._dims, self.__numbered_squares, self.__walls))

    @property
    def number_of_edges(self) -> int:
        """
        The number of edges on grid.
        
        Returns:
            The total number of edges on game grid.
        """
        m = self._height
        n = self._width
        return 2*m*n - m - n

    @property
    def numbered_squares(self) -> list[tuple[int, int]]:
        return self.__numbered_squares

    def __set_numbered_squares(self, values: list[tuple[int, int]]) -> None:

        if not isinstance(values, list):
            msg = f"The numbered squares must be a list of tuples. Got a {type(values).__name__} instead."
            raise TypeError(msg)

        if len(values) > len(self):
            msg = (
                "The quantity of numbered squares exceeds the amount of grid squares."
                f" Got {len(values)} squares, while the grid has {len(self)} squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of numbered squares is too small for the game."
                f" Got a total of {len(values)} numbered squares."
            )
            raise ValueError(msg)

        if len(values) != len(set(values)):
            msg = "The numbered squares list has duplicated squares."
            raise ValueError(msg)

        self.__numbered_squares = values

    @property
    def walls(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return self.__walls

    def __set_walls(self, values: list[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
        if values is None:
            self.__walls = []
            return

        if len(values) > self.number_of_edges:
            msg = (
                "The number of walls exceeds the amount of grid edges."
                f" Got {len(values)} numbered squares,"
                f" but the grid has {self.number_of_edges} squares."
            )
            raise ValueError(msg)

        if not isinstance(values, (list, tuple, set)):
            msg = f"Walls must be a tuple, list or set of squares. Got a {type(values).__name__} instead."
            raise TypeError(msg)

        invalid_items = [pair for pair in values if TaxicabDistance.calculate(*pair) != 1]
        if invalid_items:
            msg = f"Squares in a pair must be consecutive ones. Invalid pairs: {invalid_items!r}."
            raise ValueError(msg)

        self.__walls = sorted(set(values))


    def set_solution(self, value: GameSolution) -> None:
        if not isinstance(value, ZipSolution):
            msg = f"Invalid input. Got a {type(value).__name__} object."
            raise TypeError(msg)
        self._solution = value

    @property
    def squares(self) -> dict[tuple[int, int], int | None]:
        if self._solution:
            return self._solution.squares
        numbered_squares = {square: i+1 for i, square in enumerate(self.__numbered_squares)}
        return {
            (i, j): numbered_squares.get((i, j))
            for i in range(1, self._height+1)
            for j in range(1, self._width+1)
        }

    @property
    def edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        if self._solution:
            return self._solution.edges
        I = range(1, self._height+1)
        J = range(1, self._width+1)
        edges = [((i,j), (i+1, j)) for i in I for j in J if i+1 in I]
        edges += [((i,j), (i-1, j)) for i in I for j in J if i-1 in I]
        edges += [((i,j), (i, j+1)) for i in I for j in J if j+1 in J]
        edges += [((i,j), (i, j-1)) for i in I for j in J if j-1 in J]
        return dict.fromkeys(edges, 0)

    @property
    def path(self) -> list[tuple[int, int]]:
        if self._solution:
            return self._solution.path
        return []

    @property
    def solution(self) -> list[tuple[int, int]]:
        return self.path
