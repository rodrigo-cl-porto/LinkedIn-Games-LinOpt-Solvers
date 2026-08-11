import pyomo.environ as pyo
from ._rectangle_seed import RectangleSeed
from ._rectangle_shape import RectangleShape


class PatchesModel(pyo.ConcreteModel):
    """The Linear Optimization model for the Patches game."""

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
        V = self.V = pyo.Set( # Vertical rectangles
            initialize=[seed.color_code for seed in seeds if seed.shape == RectangleShape.VERTICAL], domain=K
        )
        H = self.H = pyo.Set( # Horizontal rectangles
            initialize=[seed.color_code for seed in seeds if seed.shape == RectangleShape.HORIZONTAL], domain=K
        )
        Q = self.Q = pyo.Set( # Squared rectangles
            initialize=[seed.color_code for seed in seeds if seed.shape == RectangleShape.SQUARE], domain=K
        )
        A = self.A = pyo.Set( # Rectangles with required area
            initialize=[seed.color_code for seed in seeds if seed.area is not None], domain=K
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

        ## Contiguity constraints
        self.row_contiguity_constraints = pyo.Constraint(
            pyo.RangeSet(1, m-2), pyo.RangeSet(3, m), K, rule=lambda model, i1, i2, k:
                u[i1, k] - pyo.quicksum(u[i,k] for i in range(i1+1, i2)) + u[i2, k] <= 1
                if i2 - i1 > 1 else pyo.Constraint.Skip
        )
        self.column_contiguity_contraints = pyo.Constraint(
            pyo.RangeSet(1, n-2), pyo.RangeSet(3, n), K, rule=lambda model, j1, j2, k:
                v[j1, k] - pyo.quicksum(v[j,k] for j in range(j1+1, j2)) + v[j2, k] <= 1
                if j2 - j1 > 1 else pyo.Constraint.Skip
        )

        ## McCormick Linearization constraints
        self.cutout_row_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i,j,k] <= u[i,k]
        )
        self.cutout_column_constraints = pyo.Constraint(
            I, J, K, rule=lambda model, i, j, k: x[i,j,k] <= v[j,k]
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
        self.vertical_rectangles_constraints = pyo.Constraint(
            V, rule=lambda model, k: pyo.quicksum(u[i,k] for i in I) >= pyo.quicksum(v[j,k] for j in J) + 1
        )
        self.horizontal_rectangles_constraints = pyo.Constraint(
            H, rule=lambda model, k: pyo.quicksum(v[j,k] for j in J) >= pyo.quicksum(u[i,k] for i in I) + 1
        )
        self.square_rectangles_constraints = pyo.Constraint(
            Q, rule=lambda model, k: pyo.quicksum(u[i,k] for i in I) == pyo.quicksum(v[j,k] for j in J)
        )
