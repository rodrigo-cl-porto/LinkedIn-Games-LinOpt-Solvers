from .._shared.domain.game_facade import GameFacade
from ._game_grid import TangoGrid


class Tango(GameFacade):
    """The [LinkedIn Tango](https://www.linkedin.com/games/tango/) game.
    
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
    _game: TangoGrid

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
        super().__init__(6, filled_squares, matching_pairs, opposite_pairs)

    def _set_game(self,
            filled_squares: dict[tuple[int, int], int],
            matching_pairs:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None = None,
            opposite_pairs:
                set[tuple[tuple[int, int], tuple[int, int]]]
                | list[tuple[tuple[int, int], tuple[int, int]]]
                | None = None
        ) -> None:
        self._game = TangoGrid(
            dims=self.dims,
            filled_squares=filled_squares,
            matching_pairs=matching_pairs,
            opposite_pairs=opposite_pairs
        )

    @property
    def filled_squares(self) -> dict[tuple[int, int], int]:
        """Squares that are already filled with a symbol.
        
        Returns:
            Starting filled squares as a dictionary of `(row, column): 0 | 1` items.
        """
        return self._game.filled_squares

    @property
    def matching_pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Pairs of matching squares.

        Pairs of squares that are separated by a `=` sign, i.e., that must have the same symbols.

        Returns:
            Pairs of matching squares as a set of `((row1, column1), (row2, column2))`.
        """
        return self._game.matching_pairs

    @property
    def opposite_pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Pairs of opposite squares.

        Pairs of squares that are separated by a `×` sign, i.e., that must have opposite symbols.

        Returns:
            Pairs of opposite squares as a set of `((row1, column1), (row2, column2))` items.
        """
        return self._game.opposite_pairs

    @property
    def moons(self) -> list[tuple[int, int]]:
        """All the squares filled with moons.

        Returns:
            A list of all moon squares as `(row, column)`.
        """
        return self._game.moons

    @property
    def suns(self) -> list[tuple[int, int]]:
        """All the squares filled with suns.
        
        Returns:
            A list of all sun squares as `(row, column)`.
        """
        return self._game.suns
