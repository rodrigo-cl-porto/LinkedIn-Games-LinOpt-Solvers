from ....patches._game_grid import PatchesGrid
from ....patches._renderer import PatchesRenderer
from ....queens._game_grid import QueensGrid
from ....queens._renderer import QueensRenderer
from ....shikaku._game_grid import ShikakuGrid
from ....shikaku._renderer import ShikakuRenderer
from ....sudoku._game_grid import SudokuGrid
from ....sudoku._renderer import SudokuRenderer
from ....tango._game_grid import TangoGrid
from ....tango._renderer import TangoRenderer
from ....zip._game_grid import ZipGrid
from ....zip._renderer import ZipRenderer
from ...domain.game_grid import GameGrid
from ._renderer import GameRenderer


class GameRendererFactory:
    @staticmethod
    def create_renderer(game: GameGrid) -> GameRenderer:
        if isinstance(game, PatchesGrid):
            return PatchesRenderer(game)
        
        if isinstance(game, QueensGrid):
            return QueensRenderer(game)

        if isinstance(game, ShikakuGrid):
            return ShikakuRenderer(game)

        if isinstance(game, SudokuGrid):
            return SudokuRenderer(game)
        
        if isinstance(game, TangoGrid):
            return TangoRenderer(game)

        if isinstance(game, ZipGrid):
            return ZipRenderer(game)

        msg = f"Invalid game. Got {type(game).__name__} instead."
        raise TypeError(msg)
