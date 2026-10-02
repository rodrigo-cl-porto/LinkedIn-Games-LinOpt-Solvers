from ....patches._renderer import PatchesRenderer
from ....queens._renderer import QueensRenderer
from ....shikaku._renderer import ShikakuRenderer
from ....sudoku._renderer import SudokuRenderer
from ....tango._renderer import TangoRenderer
from ....zip._renderer import ZipRenderer
from ...domain.game_grid import GameGrid
from .renderer import GameRenderer


class GameRendererFactory:
    @staticmethod
    def create_renderer(game: GameGrid) -> GameRenderer:
        match type(game).__name__:
            case "PatchesGrid":
                return PatchesRenderer(game)
            case "QueensGrid":
                return QueensRenderer(game)
            case "ShikakuGrid":
                return ShikakuRenderer(game)
            case "SudokuGrid":
                return SudokuRenderer(game)
            case "TangoGrid":
                return TangoRenderer(game)
            case "ZipGrid":
                return ZipRenderer(game)
            case _:
                msg = f"Invalid game. Got {type(game).__name__} instead."
                raise TypeError(msg)
