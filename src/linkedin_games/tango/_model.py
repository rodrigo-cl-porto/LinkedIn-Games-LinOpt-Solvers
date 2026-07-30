import pyomo.environ as pyo


class TangoModel(pyo.ConcreteModel):
    """The Linear Optimization Model for Tango game."""

    def __init__(self,
            board_dims: tuple[int, int],
            filled_squares: dict[tuple[int, int]: int] | None = None,
            matching_pairs: set[tuple[tuple[int, int], tuple[int, int]]] | None = None,
            opposite_pairs: set[tuple[tuple[int, int], tuple[int, int]]] | None = None) -> None:
        """
        Args:
            board_dims: Board dimensions as a `(row, column)` tuple.
            filled_squares: Starting filled squares as a dictionary of `(row, column): 0 | 1`.
            matching_pairs: Pairs of matching squares (separated by a `=` sign)
                as a set of `((row1, column1), (row2, column2))`.
            opposite_pairs: Pairs of opposite squares (separated by a `×` sign)
                as a set of `((row1, column1), (row2, column2))`.
        """
        super().__init__()

        # BOARD DIMENSIONS
        m, n = board_dims
        self.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = self.I = pyo.RangeSet(n) # Rows
        J = self.J = pyo.RangeSet(m) # Columns

        # COMPOSITE SETS
        S = self.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        K = self.K = pyo.Set(initialize=filled_squares.keys(), dimen=2)
        M = self.M = pyo.Set(initialize=matching_pairs)
        O = self.O = pyo.Set(initialize=opposite_pairs)

        # DECISION VARIABLES
        x = self.x = pyo.Var(S, within=pyo.Binary)

        # PARAMETERS
        m = self.m # Total number of rows
        n = self.n # Total number of columns
        k = self.k = pyo.Param(K, initialize=filled_squares, within=pyo.Binary) # Filled values

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0) # feasibility problem

        # CONSTRAINTS
        self.equal_moons_suns_per_row_constraints = pyo.Constraint(
            I, rule=lambda model, i: sum(x[i, j] for j in J) == n / 2
        )
        self.equal_moons_suns_per_column_constraints = pyo.Constraint(
            J, rule=lambda model, j: sum(x[i,j] for i in I) == m / 2
        )
        self.no_three_consecutive_moons_per_row_constraints = pyo.Constraint(
            I, pyo.RangeSet(n-2),
            rule=lambda model, i, j: x[i, j] + x[i, j+1] + x[i, j+2] <= 2
        )
        self.no_three_consecutive_suns_per_row_constraints = pyo.Constraint(
            I, pyo.RangeSet(n-2),
            rule=lambda model, i, j: x[i, j] + x[i, j+1] + x[i, j+2] >= 1
        )
        self.no_three_consecutive_moons_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(m-2), J,
            rule=lambda model, i, j: x[i, j] + x[i+1, j] + x[i+2, j] <= 2
        )
        self.no_three_consecutive_suns_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(m-2), J,
            rule=lambda model, i, j: x[i, j] + x[i+1, j] + x[i+2, j] >= 1
        )
        self.matching_pairs_constraints = pyo.Constraint(
            M, rule=lambda model, i, j, r, s: x[i, j] - x[r, s] == 0
        )
        self.opposite_pairs_constraints = pyo.Constraint(
            O, rule=lambda model, i, j, r, s: x[i, j] + x[r, s] == 1
        )
        self.already_filled_squares_constraints = pyo.Constraint(
            K, rule=lambda model, i, j: x[i, j] == k[i, j]
        )
