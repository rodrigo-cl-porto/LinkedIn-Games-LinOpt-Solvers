import pyomo.environ as pyo

from ._region import Region


class QueensModel(pyo.ConcreteModel):
    """The Linear Optimization model for the Queens game"""
    def __init__(self, board_dims:tuple[int, int], regions:set[Region]):
        super().__init__()

        # BOARD DIMENSIONS
        m, n = board_dims
        self.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = self.I = pyo.RangeSet(n) # Rows
        J = self.J = pyo.RangeSet(m) # Columns
        K = self.K = pyo.Set(initialize=[region.color for region in regions]) # Colored Regions

        # COMPOSITE SETS
        S = self.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        R = self.R = pyo.Set(  # Region Squares
            K,
            initialize={region.color: region.squares for region in regions},
            dimen=2,
        )
        D = self.D = pyo.Set(initialize=lambda model: # Diagonals
            [((i, j), (i + 1, j + 1)) for (i, j) in S if (i + 1, j + 1) in S] +
            [((i, j), (i + 1, j - 1)) for (i, j) in S if (i + 1, j - 1) in S]
        )

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0)  # feasibility problem

        # DECISION VARIABLES
        x = self.x = pyo.Var(S, within=pyo.Binary, initialize=0)

        # CONSTRAINTS
        self.single_crown_per_row_constraints = pyo.Constraint(
            I, rule=lambda model, i: sum(x[i, j] for j in J) == 1
        )
        self.single_crown_per_column_constraints = pyo.Constraint(
            J, rule=lambda model, j: sum(x[i, j] for i in I) == 1
        )
        self.single_crown_per_region_constraints = pyo.Constraint(
            K, rule=lambda model, k: sum(x[i, j] for (i, j) in R[k]) == 1
        )
        self.adjacent_squares_by_vertex_constraints = pyo.Constraint(
            D, rule=lambda model, i, j, r, s: x[i, j] + x[r, s] <= 1
        )
