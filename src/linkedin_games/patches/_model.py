import pyomo.environ as pyo


class PatchesModel(pyo.ConcreteModel):
    """The Linear Optimization model for the Patches game."""

    def __init__(self, board_dims: tuple[int, int], seeds: dict[tuple[int, int], dict[str, str|int]]) -> None:
        """
        Args:
            board_dims: Board dimensionas as `(rows, columns)` tuple.
            seeds: Rectangle seeds on board as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}`.
        """
        super().__init__()

        # BOARD DIMENSIONS
        m, n = board_dims
        self.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = self.I = pyo.RangeSet(n) # Rows
        J = self.J = pyo.RangeSet(m) # Columns
        K = self.K = pyo.Set(initialize=(seed["color"] for seed in seeds.values())) # Rectangles

        # COMPOSITE SETS
        S = self.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        E = self.E = pyo.Set(initialize=[(*square, seed["color"]) for square, seed in seeds.items()]) # Rectangle Seeds
        V = self.V = pyo.Set(initialize=[ # Vertical rectangles
            seed["color"] for seed in seeds.values() if seed["shape"] == "vertical"
        ])
        H = self.H = pyo.Set(initialize=[ # Horizontal rectangles
            seed["color"] for seed in seeds.values() if seed["shape"] == "horizontal"
        ])
        Q = self.Q = pyo.Set(initialize=[ # Squared rectangles
            seed["color"] for seed in seeds.values() if seed["shape"] == "square"
        ])
        A = self.A = pyo.Set(initialize=[ # Rectangles with required area
            seed["color"] for seed in seeds.values() if seed["area"] is not None
        ])

        # DECISION VARIABLES
        ## Integer variables
        l = self.l = pyo.Var(K, domain=pyo.PositiveIntegers) # Index of the leftmost column of the rectangle k
        t = self.t = pyo.Var(K, domain=pyo.PositiveIntegers) # Index of the top row of the rectangle k
        w = self.w = pyo.Var(K, domain=pyo.PositiveIntegers) # Width of rectangle k
        h = self.h = pyo.Var(K, domain=pyo.PositiveIntegers) # Height of rectangle k

        ## Binary variables
        u = self.u = pyo.Var(I, K, domain=pyo.Binary, initialize=0) # u_ik = 1 if row i passes through rectangle k
        v = self.v = pyo.Var(J, K, domain=pyo.Binary, initialize=0) # v_jk = 1 if column j passes through rect k
        x = self.x = pyo.Var(I, J, K, domain=pyo.Binary, initialize=0) # x_ijk = 1 if square (i,j) is covered by rect k

        # PARAMETERS
        a = self.a = pyo.Param( # Required areas
            K, initialize={seed["color"]: seed["area"] for seed in seeds.values() if seed["area"] is not None}
        )

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=sum(w[k] + h[k] for k in K), sense=pyo.minimize)

        # CONSTRAINTS
        ## Non overlapping rectangles
        self.unique_rectangle_per_square_constraints = pyo.Constraint(
            S, rule=lambda model, i, j: sum(x[i, j, k] for k in K) == 1
        )

        ## Board-Boundaries Constraints
        self.top_row_constraints = pyo.Constraint(
            K, rule=lambda model, k: t[k] + h[k] - 1 <= m
        )
        self.leftmost_column_constraints = pyo.Constraint(
            K, rule=lambda model, k: l[k] + w[k] - 1 <= n
        )

        ## Boundaries Constraints
        self.top_boundary_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, k: t[k] - i <= m * (1 - u[i, k])
        )
        self.bottom_boundary_constraints = pyo.Constraint(
            I, K, rule=lambda model, i, k: i - (t[k] + h[k] - 1) <= m * (1 - u[i, k])
        )
        self.left_boundary_constraints = pyo.Constraint(
            J, K, rule=lambda model, j, k: l[k] - j <= n * (1 - v[j, k])
        )
        self.right_boundary_constraints = pyo.Constraint(
            J, K, rule=lambda model, j, k: j - (l[k] + w[k] - 1) <= n * (1 - v[j, k])
        )

        ## Linking-Binary-Variables Constraints
        self.cutout_row_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i, j, k] <= u[i, k]
        )
        self.cutout_column_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i, j, k] <= v[j, k]
        )
        self.square_activator_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i, j, k] >= u[i, k] + v[j, k] - 1
        )

        ## Seed Square Constraints
        self.seed_square_coverage_constraints = pyo.Constraint(
            E, rule=lambda model, i, j, k: x[i, j, k] == 1
        )
        self.area_constraints = pyo.Constraint(  # Required area
            A, rule=lambda model, k: sum(x[i, j, k] for (i, j) in S) == a[k]
        )
        self.vertical_rectangles_constraints = pyo.Constraint(
            V, rule=lambda model, k: w[k] <= h[k] - 1
        )
        self.horizontal_rectangles_constraints = pyo.Constraint(
            H, rule=lambda model, k: w[k] >= h[k] + 1
        )
        self.square_rectangles_constraints = pyo.Constraint(
            Q, rule=lambda model, k: w[k] == h[k]
        )
