from ...domain.games.game_grid import GameGrid
from ._builder import GameSolutionBuilder
from .patches import PatchesSolutionBuilder
from .queens import QueensSolutionBuilder
from .shikaku import ShikakuSolutionBuilder
from .sudoku import SudokuSolutionBuilder
from .tango import TangoSolutionBuilder
from .zip import ZipSolutionBuilder


class GameSolutionBuilderFactory:
    @staticmethod
    def create_builder(game: GameGrid) -> GameSolutionBuilder:
        match type(game).__name__:
            case "Patches":
                return PatchesSolutionBuilder()
            case "Queens":
                return QueensSolutionBuilder()
            case "Shikaku":
                return ShikakuSolutionBuilder()
            case "BaseSudoku":
                return SudokuSolutionBuilder()
            case "Tango":
                return TangoSolutionBuilder()
            case "Zip":
                return ZipSolutionBuilder()
            case _:
                msg = f"Invalid game. Got {type(game).__name__} instead."
                raise TypeError(msg)
