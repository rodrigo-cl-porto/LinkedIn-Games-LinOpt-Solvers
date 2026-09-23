from ...domain.games.patches.patches import Patches
from ..builders.patches import PatchesModelBuilder
from ._director import OptimizationModelDirector


class PatchesModel(OptimizationModelDirector[Patches]):
    def _set_builder(self, game: Patches) -> None:
        self._builder = PatchesModelBuilder(game)
