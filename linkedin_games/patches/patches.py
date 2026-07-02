from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..gameboard import GameBoard
from .rectangle import TipSeed, Rectangle, RecType


class Patches(GameBoard):

    """
    A class representing a Patches board game with colored rectangles.
    """

    def __init__(self, board_dims: tuple[int, int], tip_seeds: tuple[TipSeed]):
        super().__init__(board_dims)
        self.tip_seeds = tip_seeds
    

    def __hash__(self) -> int:
        return hash((self.board_dims, self.tip_seeds))


    @property
    def tip_seeds(self) -> tuple[TipSeed]:
        return self._tip_seeds

    @tip_seeds.setter
    def tip_seeds(self, value: tuple[TipSeed]) -> None:
        
        if len(value) < 1:
            msg = "The tip seeds cannot be empty!"
            raise ValueError(msg)
        
        invalid_items = [item for item in value if not isinstance(item, TipSeed)]
        if invalid_items:
            msg = f"Tip seeds must be a tuple of TipSeed classes. Got the following invalid items: {invalid_items!r}."
            raise TypeError(msg)
        
        if len(value) != len({tip.color for tip in value}):
            msg = "There must not be two tip seeds with the same color."
            raise ValueError(msg)
        
        seed_squares = [tip.seed_square for tip in value]
        duplicated_squares = [square for square in seed_squares if seed_squares.count(square) > 1]
        if duplicated_squares:
            msg = (
                "The seed squares must not overlap each other.\n"
                f"The following squares are duplicated: {duplicated_squares}"
            )
            raise ValueError(msg)

        if not isinstance(value, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, the collection of TipSeeds should be a tuple."
                f"Got a {type(value)} instead."
            ))
            value = tuple(value)
        
        self._tip_seeds = value
        self._stale = True


    @property
    def rectangles(self) -> tuple[Rectangle]:
        return self._rectangles


    def _construct_model(self) -> None:
        model = self.model

        # RANGE SETS
        I = model.I # Rows
        J = model.J # Columns
        K = model.K = pyo.Set(initialize=(tip.color for tip in self.tip_seeds)) # Rectangle Tips

        # COMPOSITE SETS
        S = model.S # Board squares
        T = model.T = pyo.Set(initialize=[(*tip.seed_square, tip.color) for tip in self.tip_seeds]) # Set of triples (i,j,k) indicating tip square (i,j) for rectangle k
        V = model.V = pyo.Set(initialize=[tip.color for tip in self.tip_seeds if tip.rect_type == RecType.VERTICAL])
        H = model.H = pyo.Set(initialize=[tip.color for tip in self.tip_seeds if tip.rect_type == RecType.HORIZONTAL])
        Q = model.Q = pyo.Set(initialize=[tip.color for tip in self.tip_seeds if tip.rect_type == RecType.SQUARE])
        A = model.A = pyo.Set(initialize=[tip.color for tip in self.tip_seeds if tip.rect_type is not None])

        # DECISION VARIABLES
        x = model.x = pyo.Var(I, J, K, domain=pyo.Binary)
        c = model.c = pyo.Var(K, domain=pyo.PositiveIntegers) # Column index of first cell of rectangle k
        r = model.r = pyo.Var(K, domain=pyo.PositiveIntegers) # Row index of first cell of rectangle k
        w = model.w = pyo.Var(K, domain=pyo.PositiveIntegers) # Width of rectangle k
        h = model.h = pyo.Var(K, domain=pyo.PositiveIntegers) # Height of rectangle k

        # PARAMETERS: tip area for those rectangles that specify it
        m = model.m # Total number of rows
        n = model.n # Total number of columns
        a = model.a = pyo.Param( # Preset areas
            K,
            initialize= {tip.color: tip.seed_area for tip in self.tip_seeds if tip.seed_area is not None}
        )

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=sum(w[k] + h[k] for k in K), sense=pyo.minimize)

        # CONSTRAINTS
        # Non overlapping rectangles
        model.unique_rectangle_per_square_constraints = pyo.Constraint(
            S,
            rule=lambda model, i, j: sum(x[i, j, k] for k in K) == 1
        )

        # Rectangle inside board
        model.last_row_position_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: r[k] + h[k] - 1 <= m
        )
        model.last_column_position_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: c[k] + w[k] - 1 <= n
        )

        # Coverage constraints (if x[i,j,k]=1 then row/col must be within r..r+h-1 etc.)
        model.row_lower_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: r[k] - i <= m * (1 - x[i, j, k])
        )
        model.row_upper_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: i - (r[k] + h[k] - 1) <= m * (1 - x[i, j, k])
        )
        model.column_lower_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: c[k] - j <= n * (1 - x[i, j, k])
        )
        model.column_upper_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: j - (c[k] + w[k] - 1) <= n * (1 - x[i, j, k])
        )

        # Tip Constraints
        model.seed_square_constraints = pyo.Constraint( # Seed square
            T,
            rule=lambda model, i, j, k: x[i, j, k] == 1
        ) 

        model.seed_area_constraints = pyo.Constraint( # Tip area
            A,
            rule=lambda model, k: sum(x[i, j, k] for (i, j) in S) == a[k]
        )

        # Orientation constraints
        model.vertical_rectangle_constraints = pyo.Constraint(
            V,
            rule=lambda model, k: w[k] <= h[k] - 1
        )
        model.horizontal_rectangle_constraints = pyo.Constraint(
            H,
            rule=lambda model, k: w[k] >= h[k] + 1
        )
        model.square_rectangle_constraints = pyo.Constraint(
            Q,
            rule=lambda model, k: w[k] == h[k]
        )


    def _set_solution(self, verbose:bool=False) -> None:

        self._rectangles = tuple(
            Rectangle(
                color=tip.color,
                seed_square=tip.seed_square,
                seed_area=tip.seed_area,
                rect_type= tip.rect_type,
                x = int(round(pyo.value(self.model.c[tip.color]), 0)),
                y = int(round(pyo.value(self.model.r[tip.color]), 0)),
                width = int(round(pyo.value(self.model.w[tip.color]), 0)),
                height = int(round(pyo.value(self.model.h[tip.color]), 0))
            ) for tip in self.tip_seeds
        )

        nx.set_node_attributes(
            self.board,
            name="color",
            values={(i-1, j-1): rectangle.color for rectangle in self.rectangles for (i, j) in rectangle.squares}
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
