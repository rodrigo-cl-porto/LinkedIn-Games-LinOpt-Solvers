import pyomo.environ as pyo


class SudokuModel(pyo.ConcreteModel):
    """A Linear Optimization Model for a general Sudoku game."""

    def __init__(self,
            board_dims: tuple[int, int],
            block_dims: tuple[int, int],
            filled_squares: dict[tuple[int, int], int]) -> None:
        """
        Args:
            board_dims: Board dimensions as a `(rows, columns)` tuple.
            block_dims: Grid block dimensions as a `(rows, columns)` tuple.
            filled_squares: Starting filled squares as a dictionary of `(row, column): digit` values.
        """
        super().__init__()

        # BOARD AND BLOCK DIMENSIONS
        m, n = board_dims
        p, q = block_dims
        self.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)
        self.p = pyo.Param(initialize=p, within=pyo.PositiveIntegers)
        self.q = pyo.Param(initialize=q, within=pyo.PositiveIntegers)
        
        # RANGE SETS
        I = self.I = pyo.RangeSet(n) # Rows
        J = self.J = pyo.RangeSet(m) # Columns
        K = self.K = pyo.RangeSet(n) # Digits
        U = self.u = pyo.RangeSet(p) # Rows per block
        V = self.v = pyo.RangeSet(q) # Columns per block

        # COMPOSITE SETS
        S = self.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        B = self.B = pyo.Set( # Grid blocks
            V, U,
            initialize= lambda model, v, u: [(i, j) for i in range(p*(v-1)+1, p*v+1) for j in range(q*(u-1)+1, q*u+1)]
        )
        F = self.F = pyo.Set(initialize=((i, j, k) for (i,j), k in filled_squares.items()), dimen=3) # Filled values
        
        # DECISION VARIABLES
        x = self.x = pyo.Var(S, K, within=pyo.Binary, initialize=0)
        
        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0) # feasible problem
        
        # CONSTRAINTS
        self.unique_digits_per_row_constraints = pyo.Constraint(
            J, K,
            rule=lambda model, j, k: sum(x[i, j, k] for i in I) == 1
        )
        self.unique_digits_per_column_constraints = pyo.Constraint(
            I, K,
            rule=lambda model, i, k: sum(x[i, j, k] for j in J) == 1
        )
        self.unique_digits_per_block_constraints = pyo.Constraint(
            V, U, K,
            rule=lambda model, v, u, k: sum(x[i, j, k] for (i, j) in B[v, u]) == 1
        )
        self.single_digit_per_square_constraints = pyo.Constraint(
            S,
            rule=lambda model, i, j: sum(x[i, j, k] for k in K) == 1
        )
        self.alreadey_filled_squares_constraints = pyo.Constraint(
            F,
            rule=lambda model, i, j, k: x[i, j, k] == 1
        )
