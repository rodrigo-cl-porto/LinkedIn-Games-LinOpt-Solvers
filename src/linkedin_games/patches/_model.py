import pyomo.environ as pyo
from ..shikaku._model import ShikakuModel
from ._patch_seed import PatchSeed
from ._patch_shape import PatchShape


class PatchesModel(ShikakuModel):
    """The Linear Optimization model for the Patches game."""

    def __init__(self, board_dims: tuple[int, int], seeds: list[PatchSeed]) -> object:
        """
        Args:
            board_dims: Board dimensionas as `(rows, columns)` tuple.
            seeds: Rectangle seeds on board as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}`.
        """
        super().__init__(board_dims, seeds)

        # RANGE SETS
        K = self.K # Rectangles

        # COMPOSITE SETS
        V = self.V = pyo.Set( # Vertical rectangles
            initialize=[seed.color_code for seed in seeds if seed.shape == PatchShape.VERTICAL], domain=K
        )
        H = self.H = pyo.Set( # Horizontal rectangles
            initialize=[seed.color_code for seed in seeds if seed.shape == PatchShape.HORIZONTAL], domain=K
        )
        Q = self.Q = pyo.Set( # Squared rectangles
            initialize=[seed.color_code for seed in seeds if seed.shape == PatchShape.SQUARE], domain=K
        )

        # DECISION VARIABLES
        ## Integer variables
        h = self.h # Height of rectangle k
        w = self.w # Width of rectangle k

        # CONSTRAINTS
        ## Rectangle Seed Constraints
        self.vertical_rectangles_constraints = pyo.Constraint(
            V, rule=lambda model, k: h[k] >= w[k] + 1
        )
        self.horizontal_rectangles_constraints = pyo.Constraint(
            H, rule=lambda model, k: w[k] >= h[k] + 1
        )
        self.square_rectangles_constraints = pyo.Constraint(
            Q, rule=lambda model, k: h[k] == w[k]
        )
