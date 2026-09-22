from ..._game_grid import GameGrid
from ...utils.taxicab_distance import TaxicabDistance


class Zip(GameGrid):
    """
    The [LinkedIn Zip](https://www.linkedin.com/games/zip/) game.
    
    A game grid with some numbered squares and walls (walls are optional).
    
    Objective:
        To trace a single path that runs through all the grid squares.

    Rule:
        The path must move through numbered squares in ascending order,
        starting from square number 1 to the one with the highest number.
    """
    def __init__(self,
            size:int,
            numbered_squares: list[tuple[int, int]],
            walls: list[tuple[tuple[int, int], tuple[int, int]]] | None = None
        ) -> None:
        """
        Args:
            size: The side length of the game.
            numbered_squares: Squares with a assigned number as a dictionary of `(row, column): number` items.
            walls: Pairs of squares separated by a walls as a set of `((row1, column1), (row2, column2))`.
        
        Raises:
            TypeError: If the types of the arguments don't match their required types.
            ValueError: If the quantity of numbered squares exceeds the total number of squares on the grid,
                or if the number of walls exceeds the total number of edges on the grid,
                or if any pair of squares in walls are not adjacent.
        """
        super().__init__(grid_dims=(size,size))
        self.__set_numbered_squares(numbered_squares)
        self.__set_walls(walls)


    def __hash__(self) -> int:
        return hash((self._grid_dims, self.__numbered_squares, self.__walls))


    @property
    def size(self) -> int:
        """The side length of the game.

        Returns:
            The number of rows (or columns) on game's grid.
        """
        return self.grid_dims[0]


    @property
    def number_of_edges(self) -> int:
        """
        The number of edges on grid.
        
        Returns:
            The total number of edges on game grid.
        """
        return self.grid.number_of_edges() / 2


    @property
    def numbered_squares(self) -> list[tuple[int, int]]:
        """
        The squares with a assigned number.

        Returns:
            The numbered squares as a dictionary of `(row, column): number` items.
        """
        return self.__numbered_squares
    
    def __set_numbered_squares(self, values:list[tuple[int, int]]) -> None:

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

        if not isinstance(values, list):
            msg = f"The numbered squares must be a list of tuples. Got a {type(values).__name__} instead."
            raise TypeError(msg)

        self.__numbered_squares = values
        nx.set_node_attributes(
            self.grid,
            name="value",
            values= {square: index for index, square in enumerate(values)}
        )


    @property
    def walls(self) -> list[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        The pairs of squares separated by a wall.
        
        Returns:
            All the grid edges blocked by a wall as a tuple of `((row1, column1), (row2, column2))`.
        """
        return self.__walls

    
    def __set_walls(self,
            values:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]] | None
        ) -> None:
        
        if values is None:
            self.__walls = None
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

        self.__walls = list(set(values))
