import pyomo.environ as pyo
from ._rectangle_seed import RectangleSeed


class ShikakuModel(pyo.ConcreteModel):
    """The Linear Optimization model for the Shikaku game."""

    def __init__(self, board_dims: tuple[int, int], seeds: list[RectangleSeed]) -> object:
        """
        Args:
            board_dims: Board dimensionas as `(rows, columns)` tuple.
            seeds: Rectangle seeds on board as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}`.
        """
        super().__init__()

        # BOARD DIMENSIONS
        m, n = board_dims
        self.m = pyo.Param(initialize=m, domain=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, domain=pyo.PositiveIntegers)

        # RANGE SETS
        I = self.I = pyo.RangeSet(m) # Rows
        J = self.J = pyo.RangeSet(n) # Columns
        K = self.K = pyo.Set(initialize=(seed.color_code for seed in seeds)) # Rectangles

        # COMPOSITE SETS
        S = self.S = pyo.Set(initialize=lambda model: [(i,j) for i in I for j in J]) # Board Squares
        E = self.E = pyo.Set(initialize=[(*seed.square, seed.color_code) for seed in seeds]) # Rectangle Seeds
        A = self.A = pyo.Set( # Rectangles with required area
            initialize=[seed.color_code for seed in seeds if seed.area is not None], domain=K
        )

        # DECISION VARIABLES
        ## Integer variables
        t = self.t = pyo.Var( # Index of the top row of the rectangle k
            K, domain=pyo.PositiveIntegers, initialize=1, bounds=(1, m)
        )
        l = self.l = pyo.Var( # Index of the leftmost column of the rectangle k
            K, domain=pyo.PositiveIntegers, initialize=1, bounds=(1, n)
        )
        h = self.h = pyo.Var( # Height of rectangle k
            K, domain=pyo.PositiveIntegers, initialize=1, bounds=(1, m)
        )
        w = self.w = pyo.Var( # Width of rectangle k
            K, domain=pyo.PositiveIntegers, initialize=1, bounds=(1, n)
        )

        ## Binary variables
        u = self.u = pyo.Var(I, K, domain=pyo.Binary, initialize=0) # u_ik = 1 if row i passes through rectangle k
        v = self.v = pyo.Var(J, K, domain=pyo.Binary, initialize=0) # v_jk = 1 if column j passes through rect k
        x = self.x = pyo.Var(I, J, K, domain=pyo.Binary, initialize=0) # x_ijk = 1 if square (i,j) is covered by rect k

        # PARAMETERS
        a = self.a = pyo.Param( # Required areas
            K, domain=pyo.PositiveIntegers,
            initialize={seed.color_code: seed.area for seed in seeds if seed.area is not None}
        )

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0) # feasibility problem

        # CONSTRAINTS
        ## Non overlapping rectangles
        self.unique_rectangle_per_square_constraints = pyo.Constraint(
            S, rule=lambda model, i, j: pyo.quicksum(x[i, j, k] for k in K) == 1
        )

        ## Board Boundaries Constraints
        self.bottom_row_constraints = pyo.Constraint(
            K, rule=lambda model, k: t[k] + h[k] - 1 <= m
        )
        self.rightmost_column_constraints = pyo.Constraint(
            K, rule=lambda model, k: l[k] + w[k] - 1 <= n
        )
        
        ## Rectangle Boundaries Constraints
        self.top_boundary_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, k: t[k] - i <= m * (1 - u[i,k])
        )
        self.bottom_boundary_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, k: i - (t[k] + h[k] - 1) <= m * (1 - u[i,k])
        )
        self.left_boundary_constraints = pyo.Constraint(
            J, K, rule=lambda model, j, k: l[k] - j <= n * (1 - v[j,k])
        )
        self.right_boundary_constraints = pyo.Constraint(
            J, K, rule=lambda model, j, k: j - (l[k] + w[k] - 1) <= n * (1 - v[j,k])
        )

        ## Rectangle Dimensions constraints
        self.height_constraints = pyo.Constraint(
            K, rule=lambda model, k: pyo.quicksum(u[i,k] for i in I) == h[k]
        )
        self.width_constraints = pyo.Constraint(
            K, rule=lambda model, k: pyo.quicksum(v[j,k] for j in J) == w[k]
        )

        ## McCormick Linearization constraints
        self.cutout_row_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, j, k: pyo.quicksum(x[i,j,k] for j in J) <= m * u[i,k]
        )
        self.cutout_column_constraints = pyo.Constraint(
            J, K, rule=lambda model, i, j, k: pyo.quicksum(x[i,j,k] for i in I) <= n * v[j,k]
        )
        self.square_activation_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i,j,k] >= u[i,k] + v[j,k] - 1
        )

        ## Rectangle Seed Constraints
        self.seed_square_constraints = pyo.Constraint(
            E, rule=lambda model, i, j, k: x[i,j,k] == 1
        )
        self.area_constraints = pyo.Constraint( # Required areas
            A, rule=lambda model, k: pyo.quicksum(x[i, j, k] for (i, j) in S) == a[k]
        )
