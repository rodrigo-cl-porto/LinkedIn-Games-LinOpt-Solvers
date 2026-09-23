from ...domain.games.shikaku.shikaku import Shikaku
from ..builders.shikaku import ShikakuModelBuilder
from ._director import OptimizationModelDirector


class ShikakuModel(OptimizationModelDirector[Shikaku]):
    def _set_builder(self, game: Shikaku) -> None:
        self._builder = ShikakuModelBuilder(game)
