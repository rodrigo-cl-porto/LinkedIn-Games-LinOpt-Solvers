from ...domain.games.queens.queens import Queens
from ..builders.queens import QueensModelBuilder
from ._director import OptimizationModelDirector


class QueensModel(OptimizationModelDirector[Queens]):
    def _set_builder(self, game: Queens) -> None:
        self._builder = QueensModelBuilder(game)
