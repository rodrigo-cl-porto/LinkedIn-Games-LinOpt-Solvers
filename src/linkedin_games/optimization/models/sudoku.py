from ...domain.games.sudoku._base import BaseSudoku
from ..builders.sudoku import SudokuModelBuilder
from ._director import OptimizationModelDirector


class SudokuModel(OptimizationModelDirector[BaseSudoku]):
    def _set_builder(self, game: BaseSudoku) -> None:
        self._builder = SudokuModelBuilder(game)
