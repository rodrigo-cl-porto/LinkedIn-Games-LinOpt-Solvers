from ...domain.games.game_grid import GameGrid
from ...domain.games.patches.patches import Patches
from ...domain.games.queens.queens import Queens
from ...domain.games.shikaku.shikaku import Shikaku
from ...domain.games.sudoku._base import BaseSudoku
from ...domain.games.tango.tango import Tango
from ...domain.games.zip.zip import Zip
from ._renderer import GameRenderer
from .patches import PatchesRenderer
from .queens import QueensRenderer
from .shikaku import ShikakuRenderer
from .sudoku import SudokuRenderer
from .tango import TangoRenderer
from .zip import ZipRenderer


class GameRendererFactory:
    @staticmethod
    def create_renderer(game: GameGrid) -> GameRenderer:
        if isinstance(game, Patches):
            return PatchesRenderer(game)
        
        if isinstance(game, Queens):
            return QueensRenderer(game)

        if isinstance(game, Shikaku):
            return ShikakuRenderer(game)

        if isinstance(game, BaseSudoku):
            return SudokuRenderer(game)
        
        if isinstance(game, Tango):
            return TangoRenderer(game)

        if isinstance(game, Zip):
            return ZipRenderer(game)

        msg = f"Invalid game. Got {type(game).__name__} instead."
        raise TypeError(msg)
