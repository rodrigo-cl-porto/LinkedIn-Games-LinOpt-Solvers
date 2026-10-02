from ....patches._opt_modeler import PatchesOptModeler
from ....queens._opt_modeler import QueensOptModeler
from ....shikaku._opt_modeler import ShikakuOptModeler
from ....sudoku._opt_modeler import SudokuOptModeler
from ....tango._opt_modeler import TangoOptModeler
from ....zip._opt_modeler import ZipOptModeler
from ...domain.game_grid import GameGrid
from .opt_modeler import OptModeler


class OptModelerFactory:
    @staticmethod
    def create_modeler(game: GameGrid) -> OptModeler:
        match type(game).__name__:
            case "PatchesGrid":
                return PatchesOptModeler()
            case "QueensGrid":
                return QueensOptModeler()
            case "ShikakuGrid":
                return ShikakuOptModeler()
            case "SudokuGrid":
                return SudokuOptModeler()
            case "TangoGrid":
                return TangoOptModeler()
            case "ZipGrid":
                return ZipOptModeler()
            case _:
                msg = f"Invalid game. Got {type(game).__name__} instead."
                raise TypeError(msg)
