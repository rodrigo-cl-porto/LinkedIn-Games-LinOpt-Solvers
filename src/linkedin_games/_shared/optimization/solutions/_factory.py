from ....patches._solution import PatchesSolution
from ....queens._solution import QueensSolution
from ....shikaku._solution import ShikakuSolution
from ....sudoku._solution import SudokuSolution
from ....tango._solution import TangoSolution
from ....zip._solution import ZipSolution
from ...domain.game_grid import GameGrid
from ._solution import GameSolution


class GameSolutionFactory:
    @staticmethod
    def create(game: GameGrid) -> GameSolution:
        match type(game).__name__:
            case "Patches":
                return PatchesSolution()
            case "Queens":
                return QueensSolution()
            case "Shikaku":
                return ShikakuSolution()
            case "BaseSudoku":
                return SudokuSolution()
            case "Tango":
                return TangoSolution()
            case "Zip":
                return ZipSolution()
            case _:
                msg = f"Invalid game. Got {type(game).__name__} instead."
                raise TypeError(msg)
