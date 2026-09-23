from ...domain.games.zip.zip import Zip
from ..builders.zip import ZipModelBuilder
from ._director import OptimizationModelDirector


class ZipModel(OptimizationModelDirector[Zip]):
    def _set_builder(self, game: Zip) -> None:
        self._builder = ZipModelBuilder(game)
