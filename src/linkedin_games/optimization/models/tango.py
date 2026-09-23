from ...domain.games.tango.tango import Tango
from ..builders.tango import TangoModelBuilder
from ._director import OptimizationModelDirector


class TangoModel(OptimizationModelDirector[Tango]):
    def _set_builder(self, game: Tango) -> None:
        self._builder = TangoModelBuilder(game)
