from ...domain.games.game_grid import GameGrid
from ...domain.games.patches.patches import Patches
from ...domain.games.queens.queens import Queens
from ...domain.games.shikaku.shikaku import Shikaku
from ...domain.games.sudoku._base import BaseSudoku
from ...domain.games.tango.tango import Tango
from ...domain.games.zip.zip import Zip
from ._builder import OptimizationModelBuilder
from .patches import PatchesModelBuilder
from .queens import QueensModelBuilder
from .shikaku import ShikakuModelBuilder
from .sudoku import SudokuModelBuilder
from .tango import TangoModelBuilder
from .zip import ZipModelBuilder


class OptimizationModelBuilderFactory:

    @staticmethod
    def create(game: GameGrid) -> OptimizationModelBuilder:

        if isinstance(game, Patches):
            return PatchesModelBuilder(game)
        
        if isinstance(game, Queens):
            return QueensModelBuilder(game)

        if isinstance(game, Shikaku):
            return ShikakuModelBuilder(game)

        if isinstance(game, BaseSudoku):
            return SudokuModelBuilder(game)
        
        if isinstance(game, Tango):
            return TangoModelBuilder(game)

        if isinstance(game, Zip):
            return ZipModelBuilder(game)

        msg = f"Invalid game. Got {type(game).__name__} instead."
        raise TypeError(msg)
