from ....patches._solution import PatchesSolution
from ....queens._solution import QueensSolution
from ....shikaku._solution import ShikakuSolution
from ....sudoku._solution import SudokuSolution
from ....tango._solution import TangoSolution
from ....zip._solution import ZipSolution
from ...domain.game_grid import GameGrid
from .solution import GameSolution


class GameSolutionFactory:
    @staticmethod
    def create(game: GameGrid) -> GameSolution:
        match type(game).__name__:
            case "PatchesGrid":
                return PatchesSolution()
            case "QueensGrid":
                return QueensSolution()
            case "ShikakuGrid":
                return ShikakuSolution()
            case "SudokuGrid":
                return SudokuSolution()
            case "TangoGrid":
                return TangoSolution()
            case "ZipGrid":
                return ZipSolution()
            case _:
                msg = f"Invalid game. Got {type(game).__name__} instead."
                raise TypeError(msg)
