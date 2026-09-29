import pyomo.environ as pyo

from ..shikaku._opt_model import ShikakuModelBuilder
from ._shape import PatchShape


class PatchesModelBuilder(ShikakuModelBuilder):

    def _set_composite_sets(self) -> None:
        super()._set_composite_sets()
        self._model.V = pyo.Set( # Vertical rectangles
            initialize=[
                seed["color_code"] for seed in self._game.seeds.values()
                if seed["shape"] == PatchShape.VERTICAL
            ],
            domain=self._model.K
        )
        self._model.H = pyo.Set( # Horizontal rectangles
            initialize=[
                seed["color_code"] for seed in self._game.seeds.values()
                if seed["shape"] == PatchShape.HORIZONTAL
            ],
            domain=self._model.K
        )
        self._model.Q = pyo.Set( # Squared rectangles
            initialize=[
                seed["color_code"] for seed in self._game.seeds.values()
                if seed["shape"] == PatchShape.SQUARE
            ],
            domain=self._model.K
        )


    def _set_rectangle_seed_constraints(self) -> None:
        super()._set_rectangle_seed_constraints()
        self._model.vertical_rectangles_constraints = pyo.Constraint(
            self._model.V,
            rule=lambda model, k: model.h[k] >= model.w[k] + 1
        )
        self._model.horizontal_rectangles_constraints = pyo.Constraint(
            self._model.H,
            rule=lambda model, k: model.w[k] >= model.h[k] + 1
        )
        self._model.square_rectangles_constraints = pyo.Constraint(
            self._model.Q,
            rule=lambda model, k: model.h[k] == model.w[k]
        )
