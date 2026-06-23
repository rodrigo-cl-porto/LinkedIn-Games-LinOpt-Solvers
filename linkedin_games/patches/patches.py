from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from rectangle import TipSeed, Rectangle, RecType


class Patches:

    """
    A class representing a Patches board game with colored rectangles.
    """

    def __init__(self, board_dims: tuple[int, int], tip_seeds: tuple[TipSeed]):
        self.board_dims = board_dims
        self.tip_seeds = tip_seeds
        self._rectangles: tuple[Rectangle] | tuple = ()
        self._model: pyo.ConcreteModel | None = None
        self._stale: bool = True # This property indicates whether the model needs to be rebuilt due to changes in the board dimensions or tip seeds.


    def __len__(self) -> int:
        m, n = self._board_dims
        return m * n
    
    def __hash__(self) -> int:
        return hash((self._board_dims, self._tip_seeds))

    @property
    def board_dims(self) -> tuple[int, int]:
        return self._board_dims

    @board_dims.setter
    def board_dims(self, value: tuple[int, int] = (1, 1)) -> None:

        if not isinstance(value, tuple):
            msg = f"Board dimensions must be a tuple, got {value!r}"
            raise ValueError(msg)
        
        if len(value) != 2:
            msg = f"Board dimensions must be a pair (m,n), got {value!r}"
            raise ValueError(msg)
        
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in value):
            msg = f"Board dimensions must be integers, got {value!r}"
            raise ValueError(msg)
        
        if any(x < 1 for x in value):
            msg = f"Board dimensions must be positive, got {value!r}"
            raise ValueError(msg)

        self._board_dims = value
        self._stale = True


    @property
    def tip_seeds(self) -> tuple[TipSeed]:
        return self._tip_seeds

    @tip_seeds.setter
    def tip_seeds(self, value: tuple[TipSeed]) -> None:

        if not isinstance(value, tuple):
            msg = f"Tip seeds must be a tuple of TipSeed classes. Got a {type(value)} instead."
            raise TypeError(msg)
        
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

        self._tip_seeds = value
        self._stale = True


    @property
    def rectangles(self) -> tuple[Rectangle]:
        return self._rectangles


    def _build_model(self) -> None:
        model = pyo.ConcreteModel()

        # INDEX SETS
        m, n = self._board_dims
        I = model.I = pyo.RangeSet(m) # Rows
        J = model.J = pyo.RangeSet(n) # Columns
        K = model.K = pyo.Set(initialize=(tip.color for tip in self.tip_seeds)) # Rectangle Tips

        # COMPOSITE SETS
        S = model.S = pyo.Set(initialize=[(i, j) for i in I for j in J])
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
        a = model.a = pyo.Param(
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

        # Attach model
        self._model = model
        self._stale = False


    def solve(self, verbose:bool = False) -> None:

        if self._stale or self._model is None:
            self._build_model()

        result = pyo.SolverFactory("highs").solve(self._model)

        if result.Solver.status == SolverStatus.ok and result.Solver.termination_condition == TerminationCondition.optimal:
            print("Optimal solution found!")

            self._rectangles = tuple(
                Rectangle(
                    color=tip.color,
                    seed_square=tip.seed_square,
                    seed_area=tip.seed_area,
                    rect_type= tip.rect_type,
                    x = int(round(pyo.value(self._model.c[tip.color]), 0)),
                    y = int(round(pyo.value(self._model.r[tip.color]), 0)),
                    width = int(round(pyo.value(self._model.w[tip.color]), 0)),
                    height = int(round(pyo.value(self._model.h[tip.color]), 0))
                ) for tip in self._tip_seeds
            )

            if verbose:
                print(self._rectangles)

        else:
            print("It was not possible to find a feasible solution for the game.")
            print(result.Solver)


    def show(self) -> None:

        if self._stale or self._model is None:
            self._build_model()

        m, n = self._board_dims
        G = nx.grid_2d_graph(m, n)
        plt.figure(figsize=(3, 3))

        color_map = [
            k
            for (i, j) in G.nodes() 
            for k in self._model.K
            if round(pyo.value(self._model.x[i+1, j+1, k]), 0) == 1 
        ]

        nx.draw(
            G,
            pos={(i, j): (j, -i) for (i, j) in G.nodes()},
            node_size=1100,
            node_shape="s",
            node_color=color_map,
            width=0,
        )
        plt.show()


if __name__ == "__main__":

    # Solving Patches No. 16
    tip_seeds = (
        TipSeed( # Yellow
            color="#846A0B",
            seed_square=(1, 2),
            rect_type=RecType.ANY,
            seed_area=2
        ),
        TipSeed( # Teal
            color="#096B78",
            seed_square=(1, 4),
            rect_type=RecType.ANY,
            seed_area=6
        ),
        TipSeed( # Purple
            color="#5A3DB1",
            seed_square=(2, 6),
            rect_type=RecType.ANY,
            seed_area=2
        ),
        TipSeed( # Green
            color="#0A7541",
            seed_square=(3, 1),
            rect_type=RecType.ANY,
            seed_area=6
        ),
        TipSeed( # Orange
            color="#EF6C00",
            seed_square=(3, 3),
            rect_type=RecType.VERTICAL,
            seed_area=2
        ),
        TipSeed( # Red
            color="#E30102",
            seed_square=(4, 4),
            rect_type=RecType.SQUARE,
            seed_area=4
        ),
        TipSeed(
            color="#097BB1",
            seed_square=(4, 6),
            rect_type=RecType.ANY,
            seed_area=2
        ), # Blue
        TipSeed( # Magenta
            color="#A01E4E",
            seed_square=(5, 1),
            rect_type=RecType.ANY,
            seed_area=2
        ),
        TipSeed( # Brick
            color="#9B3C1C",
            seed_square=(6, 3),
            rect_type=RecType.ANY,
            seed_area=6
        ),
        TipSeed( # Brown
            color="#503B36",
            seed_square=(6, 5),
            rect_type=RecType.ANY,
            seed_area=4
        )
    )

    patches = Patches((6, 6), tip_seeds)
    patches.solve(verbose=True)
    patches.show()
    print(patches.rectangles)
