from ....patches._game_grid import PatchesGrid
from ....patches._opt_model import PatchesModelBuilder
from ....queens._game_grid import QueensGrid
from ....queens._opt_model import QueensModelBuilder
from ....shikaku._game_grid import ShikakuGrid
from ....shikaku._opt_model import ShikakuModelBuilder
from ....sudoku._game_grid import SudokuGrid
from ....sudoku._opt_model import SudokuModelBuilder
from ....tango._game_grid import TangoGrid
from ....tango._opt_model import TangoModelBuilder
from ....zip._game_grid import ZipGrid
from ....zip._opt_model import ZipModelBuilder
from ...domain.game_grid import GameGrid
from .builder import OptimizationModelBuilder


class OptimizationModelBuilderFactory:

    @staticmethod
    def create(game: GameGrid) -> OptimizationModelBuilder:

        if isinstance(game, PatchesGrid):
            return PatchesModelBuilder(game)

        if isinstance(game, QueensGrid):
            return QueensModelBuilder(game)

        if isinstance(game, ShikakuGrid):
            return ShikakuModelBuilder(game)

        if isinstance(game, SudokuGrid):
            return SudokuModelBuilder(game)
        
        if isinstance(game, TangoGrid):
            return TangoModelBuilder(game)

        if isinstance(game, ZipGrid):
            return ZipModelBuilder(game)

        msg = f"Invalid game. Got {type(game).__name__} instead."
        raise TypeError(msg)
