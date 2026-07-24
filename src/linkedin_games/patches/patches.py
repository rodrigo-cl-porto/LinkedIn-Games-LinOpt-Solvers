from pprint import pprint
from typing import Self

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..game_board import GameBoard
from .rectangle import Rectangle
from .rectangle_shape import RectangleShape
from .seed_square import SeedSquare


class Patches(GameBoard):
    """A Patches board game with colorful rectangles.

    Attributes:
        board_dims (tuple[int, int]): The dimensions of the board as (rows, columns).
        seeds (tuple[SeedSquare]): All the seeds of the game.

    Methods:
        _construct_model (None): Construct the linear optimization model for the Patches game.
        _set_solution (None): Set the solution of the Patches game.
        _show (None): Show the Patches game board with rectangles.
    """
    def __init__(self, board_dims: tuple[int, int], seeds: tuple[SeedSquare]) -> Self:
        """
        Args:
            board_dims (tuple[int, int]): The dimensions of the board as (rows, columns).
            seeds (tuple[SeedSquare]): The seeds of the game.
        """
        super().__init__(board_dims)
        self.seeds = seeds

    def __hash__(self) -> int:
        return hash((self.board_dims, self.seeds))

    @property
    def seeds(self) -> tuple[SeedSquare]:
        """tuple[SeedSquare]: All the seeds of the game."""
        return self._seeds

    @seeds.setter
    def seeds(self, values: tuple[SeedSquare]) -> None:
        if len(values) < 1:
            msg = "The seeds cannot be empty!"
            raise ValueError(msg)

        invalid_items = [item for item in values if not isinstance(item, SeedSquare)]
        if invalid_items:
            msg = (
                "Seeds must be a tuple of SeedSquare classes."
                f" Got the following invalid items: {invalid_items!r}."
            )
            raise TypeError(msg)

        if len(values) != len({seed.color_code for seed in values}):
            msg = "There must not be two seeds with the same color."
            raise ValueError(msg)

        seed_squares = [seed.square for seed in values]
        duplicated_squares = [
            square for square in seed_squares if seed_squares.count(square) > 1
        ]
        if duplicated_squares:
            msg = (
                "The seed squares must not overlap each other."
                f" Duplicated squares: {duplicated_squares}"
            )
            raise ValueError(msg)

        if not isinstance(values, tuple):
            values = tuple(values)

        self._seeds = values
        self._stale = True

    @property
    def rectangles(self) -> tuple[Rectangle]:
        """All the rectangles of the Patches game."""
        return tuple(seed.rectangle for seed in self.seeds)

    def _construct_model(self) -> None:
        model = self.model

        # RANGE SETS
        I = model.I  # Rows
        J = model.J  # Columns
        K = model.K = pyo.Set(  # Rectangles
            initialize=(seed.color_code for seed in self.seeds)
        )

        # COMPOSITE SETS
        S = model.S  # Board squares
        E = model.E = pyo.Set( # Seed squares
            initialize=[(*seed.square, seed.color_code) for seed in self.seeds]
        )
        V = model.V = pyo.Set(initialize=[ # Vertical rectangles
            seed.color_code for seed in self.seeds
            if seed.shape == RectangleShape.VERTICAL
        ])
        H = model.H = pyo.Set(initialize=[ # Horizontal rectangles
            seed.color_code for seed in self.seeds
            if seed.shape == RectangleShape.HORIZONTAL
        ])
        Q = model.Q = pyo.Set(initialize=[ # Squared rectangles
            seed.color_code for seed in self.seeds
            if seed.shape == RectangleShape.SQUARE
        ])
        A = model.A = pyo.Set(initialize=[ # Required areas
            seed.color_code for seed in self.seeds if seed.area is not None
        ])

        # DECISION VARIABLES
        ## Integer variables
        l = model.l = pyo.Var( # Index of the leftmost column of the rectangle k
            K, domain=pyo.PositiveIntegers
        )
        t = model.t = pyo.Var( # Index of the top row of the rectangle k
            K, domain=pyo.PositiveIntegers
        )
        w = model.w = pyo.Var(K, domain=pyo.PositiveIntegers) # Width of rectangle k
        h = model.h = pyo.Var(K, domain=pyo.PositiveIntegers) # Height of rectangle k
        ## Binary variables
        u = model.u = pyo.Var( # u_ik = 1 if row i passes through rectangle k
            I, K, domain=pyo.Binary, initialize=0
        )
        v = model.v = pyo.Var( # v_jk = 1 if column j passes through rectangle k
            J, K, domain=pyo.Binary, initialize=0
        )  
        x = model.x = pyo.Var( # x_ijk = 1 if a square (i,j) is covered by rectangle k
            I, J, K, domain=pyo.Binary, initialize=0
        )

        # PARAMETERS
        m = model.m  # Total number of rows
        n = model.n  # Total number of columns
        a = model.a = pyo.Param(  # Required areas
            K,
            initialize={
                seed.color_code: seed.area for seed in self.seeds
                if seed.area is not None
            }
        )

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=sum(w[k] + h[k] for k in K), sense=pyo.minimize)

        # CONSTRAINTS
        ## Non overlapping rectangles
        model.unique_rectangle_per_square_constraints = pyo.Constraint(
            S, rule=lambda model, i, j: sum(x[i, j, k] for k in K) == 1
        )

        ## Board-Boundaries Constraints
        model.top_row_constraints = pyo.Constraint(
            K, rule=lambda model, k: t[k] + h[k] - 1 <= m
        )
        model.leftmost_column_constraints = pyo.Constraint(
            K, rule=lambda model, k: l[k] + w[k] - 1 <= n
        )

        ## Boundaries Constraints
        model.top_boundary_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, k: t[k] - i <= m * (1 - u[i, k])
        )
        model.bottom_boundary_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, k: i - (t[k] + h[k] - 1) <= m * (1 - u[i, k])
        )
        model.left_boundary_constraints = pyo.Constraint(
            J, K, rule=lambda model, j, k: l[k] - j <= n * (1 - v[j, k])
        )
        model.right_boundary_constraints = pyo.Constraint(
            J, K, rule=lambda model, j, k: j - (l[k] + w[k] - 1) <= n * (1 - v[j, k])
        )

        ## Linking-Binary-Variables Constraints
        model.cutout_row_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i, j, k] <= u[i, k]
        )
        model.cutout_column_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i, j, k] <= v[j, k]
        )
        model.square_activator_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i, j, k] >= u[i, k] + v[j, k] - 1
        )

        ## Seed Square Constraints
        model.seed_square_coverage_constraints = pyo.Constraint(
            E, rule=lambda model, i, j, k: x[i, j, k] == 1
        )
        model.area_constraints = pyo.Constraint(  # Required area
            A, rule=lambda model, k: sum(x[i, j, k] for (i, j) in S) == a[k]
        )
        model.vertical_rectangles_constraints = pyo.Constraint(
            V, rule=lambda model, k: w[k] <= h[k] - 1
        )
        model.horizontal_rectangles_constraints = pyo.Constraint(
            H, rule=lambda model, k: w[k] >= h[k] + 1
        )
        model.square_rectangles_constraints = pyo.Constraint(
            Q, rule=lambda model, k: w[k] == h[k]
        )

    def _set_solution(self, verbose: bool = False) -> None:
        for seed in self.seeds:
            top = round(pyo.value(self.model.t[seed.color_code]))
            left = round(pyo.value(self.model.l[seed.color_code]))
            width = round(pyo.value(self.model.w[seed.color_code]))
            height = round(pyo.value(self.model.h[seed.color_code]))
            seed._set_rectangle(
                Rectangle(
                    color=seed.color_code,
                    top_left_square=(top, left),
                    dims=(width, height),
                )
            )
        nx.set_node_attributes(
            self.board,
            name="color",
            values={
                (i - 1, j - 1): seed.color_code
                for seed in self.seeds
                for (i, j) in seed.rectangle.squares
            }
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
            node_color=[
                color for color in nx.get_node_attributes(self.board, "color").values()
            ],
            width=0
        )
        plt.show()
