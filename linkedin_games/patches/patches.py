from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..gameboard import GameBoard
from .rectangle_seed import RectangleSeed, RectangleShape
from .rectangle import Rectangle


class Patches(GameBoard):

    """
    A class representing a Patches board game with colored rectangles.
    """

    def __init__(self, board_dims: tuple[int, int], seeds: tuple[RectangleSeed]):
        super().__init__(board_dims)
        self.seeds = seeds


    def __hash__(self) -> int:
        return hash((self.board_dims, self.seeds))


    @property
    def seeds(self) -> tuple[RectangleSeed]:
        return self._seeds

    @seeds.setter
    def seeds(self, values: tuple[RectangleSeed]) -> None:
        
        if len(values) < 1:
            msg = "The seeds cannot be empty!"
            raise ValueError(msg)
        
        invalid_items = [item for item in values if not isinstance(item, RectangleSeed)]
        if invalid_items:
            msg = f"Seeds must be a tuple of RectangleSeed classes. Got the following invalid items: {invalid_items!r}."
            raise TypeError(msg)
        
        if len(values) != len({seed.color for seed in values}):
            msg = "There must not be two seeds with the same color."
            raise ValueError(msg)
        
        seed_squares = [seed.square for seed in values]
        duplicated_squares = [square for square in seed_squares if seed_squares.count(square) > 1]

        if duplicated_squares:
            msg = (
                "The seed squares must not overlap each other.\n"
                f"The following squares are duplicated: {duplicated_squares}"
            )
            raise ValueError(msg)

        if not isinstance(values, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, the collection of RectangleSeeds should be a tuple."
                f"Got a {type(values)} instead."
            ))
            values = tuple(values)
        
        self._seeds = values
        self._stale = True


    @property
    def rectangles(self) -> tuple[Rectangle]:
        return tuple(seed.rectangle for seed in self.seeds)


    def _construct_model(self) -> None:

        model = self.model

        # RANGE SETS
        I = model.I # Rows
        J = model.J # Columns
        K = model.K = pyo.Set(initialize=(seed.color for seed in self.seeds)) # Rectangle Seeds

        # COMPOSITE SETS
        S = model.S # Board squares
        E = model.E = pyo.Set(initialize=[(*seed.square, seed.color) for seed in self.seeds]) # Seed squares
        V = model.V = pyo.Set(initialize=[seed.color for seed in self.seeds if seed.shape == RectangleShape.VERTICAL])
        H = model.H = pyo.Set(initialize=[seed.color for seed in self.seeds if seed.shape == RectangleShape.HORIZONTAL])
        Q = model.Q = pyo.Set(initialize=[seed.color for seed in self.seeds if seed.shape == RectangleShape.SQUARE])
        A = model.A = pyo.Set(initialize=[seed.color for seed in self.seeds if seed.shape is not None])

        # DECISION VARIABLES
        x = model.x = pyo.Var(I, J, K, domain=pyo.Binary)
        l = model.l = pyo.Var(K, domain=pyo.PositiveIntegers) # Column index of first cell of rectangle k
        t = model.t = pyo.Var(K, domain=pyo.PositiveIntegers) # Row index of first cell of rectangle k
        w = model.w = pyo.Var(K, domain=pyo.PositiveIntegers) # Width of rectangle k
        h = model.h = pyo.Var(K, domain=pyo.PositiveIntegers) # Height of rectangle k

        # PARAMETERS
        m = model.m # Total number of rows
        n = model.n # Total number of columns
        a = model.a = pyo.Param( # Required areas
            K,
            initialize= {seed.color: seed.area for seed in self.seeds if seed.area is not None}
        )

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=sum(w[k] + h[k] for k in K), sense=pyo.minimize)

        # CONSTRAINTS
        # Non overlapping rectangles
        model.unique_rectangle_per_square_constraints = pyo.Constraint(
            S,
            rule=lambda model, i, j: sum(x[i, j, k] for k in K) == 1
        )

        # Rectangles inside board
        model.last_row_position_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: t[k] + h[k] - 1 <= m
        )
        model.last_column_position_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: l[k] + w[k] - 1 <= n
        )

        # Coverage constraints (if a square is inside a rectangle, then its coordinates must be between the rectangle dimensions)
        model.row_lower_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: t[k] - i <= m * (1 - x[i, j, k])
        )
        model.row_upper_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: i - (t[k] + h[k] - 1) <= m * (1 - x[i, j, k])
        )
        model.column_lower_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: l[k] - j <= n * (1 - x[i, j, k])
        )
        model.column_upper_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: j - (l[k] + w[k] - 1) <= n * (1 - x[i, j, k])
        )

        # Seed Constraints
        model.seed_square_constraints = pyo.Constraint( # Seed squares
            E,
            rule=lambda model, i, j, k: x[i, j, k] == 1
        )

        model.area_constraints = pyo.Constraint( # Required area
            A,
            rule=lambda model, k: sum(x[i, j, k] for (i, j) in S) == a[k]
        )

        # Orientation constraints
        model.vertical_shaped_rectangles_constraints = pyo.Constraint(
            V,
            rule=lambda model, k: w[k] <= h[k] - 1
        )
        model.horizontal_shaped_rectangles_constraints = pyo.Constraint(
            H,
            rule=lambda model, k: w[k] >= h[k] + 1
        )
        model.square_shaped_rectangles_constraints = pyo.Constraint(
            Q,
            rule=lambda model, k: w[k] == h[k]
        )


    def _set_solution(self, verbose:bool=False) -> None:

        for seed in self.seeds:
            seed._set_rectangle(
                Rectangle(
                    left = int(round(pyo.value(self.model.l[seed.color]), 0)),
                    top = int(round(pyo.value(self.model.t[seed.color]), 0)),
                    width = int(round(pyo.value(self.model.w[seed.color]), 0)),
                    height = int(round(pyo.value(self.model.h[seed.color]), 0))
                )
            )

        nx.set_node_attributes(
            self.board,
            name="color",
            values={(i-1, j-1): seed.color for seed in self.seeds for (i, j) in seed.rectangle.squares}
        )

        if verbose:
            print("These are the rectagles that solves the game:")
            pprint(self.rectangles)


    def _show(self) -> None:

        plt.figure(figsize=(3, 3))

        nx.draw(
            self.board,
            pos={(i, j): (j, -i) for (i, j) in self.board.nodes()},
            node_size=1100,
            node_shape="s",
            node_color=[color for color in nx.get_node_attributes(self.board, "color").values()],
            width=0,
        )

        plt.show()
