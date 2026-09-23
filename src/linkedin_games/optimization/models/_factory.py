from pyomo.environ import ConcreteModel

from ...domain._game_grid import GameGrid
from ...domain.games.patches.patches import Patches
from ...domain.games.queens.queens import Queens
from ...domain.games.shikaku.shikaku import Shikaku
from ...domain.games.sudoku._base import BaseSudoku
from ...domain.games.tango.tango import Tango
from ...domain.games.zip.zip import Zip
from .patches import PatchesModel
from .queens import QueensModel
from .shikaku import ShikakuModel
from .sudoku import SudokuModel
from .tango import TangoModel
from .zip import ZipModel


class OptimizationModelFactory:

    @staticmethod
    def create(game: GameGrid) -> ConcreteModel:

        if isinstance(game, Patches):
            return PatchesModel(game).build()
        
        if isinstance(game, Queens):
            return QueensModel(game).build()

        if isinstance(game, Shikaku):
            return ShikakuModel(game).build()

        if isinstance(game, BaseSudoku):
            return SudokuModel(game).build()
        
        if isinstance(game, Tango):
            return TangoModel(game).build()

        if isinstance(game, Zip):
            return ZipModel(game).build()

        msg = f"Game is invalid. Got {type(game).__name__}"
        raise TypeError(msg)
