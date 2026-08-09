import pyomo.environ as pyo


class ZipModel(pyo.ConcreteModel):
    """The Linear Optimization Model for LinkedIn Zip game."""

    def __init__(self,
            board_dims: tuple[int, int],
            numbered_squares: list[tuple[int, int]],
            walls: list[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        """
        Args:
            board_dims: Board dimensions as a `(row, column)` tuple.
            numbered_squares: Squares with a assigned number as a dictionary of `(row, column): number` items.
            walls: Pairs of squares separated by a walls as a tuple of `((row1, column1), (row2, column2))`.
        """
        super().__init__()

        # BOARD DIMENSIONS
        m, n = board_dims
        self.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = self.I = pyo.RangeSet(n) # Rows
        J = self.J = pyo.RangeSet(m) # Columns
        K = self.K = pyo.RangeSet(len(numbered_squares))

        # COMPOSITE SETS
        S = self.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        E = self.E = pyo.Set(initialize=lambda model: # Edges
            [((i,j), (i+1, j)) for i in I for j in J if i+1 in I] +
            [((i,j), (i-1, j)) for i in I for j in J if i-1 in I] +
            [((i,j), (i, j+1)) for i in I for j in J if j+1 in J] +
            [((i,j), (i, j-1)) for i in I for j in J if j-1 in J]
        )
        W = self.W = pyo.Set(initialize=walls, within=E) # Walls
        N = self.N = pyo.Set(initialize=numbered_squares, within=S)

        # DECISION VARIABLES
        x = self.x = pyo.Var(E, within=pyo.Binary, initialize=0)
        u = self.u = pyo.Var(S, within=pyo.PositiveIntegers)

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0) # feasibility problem

        # CONSTRAINTS
        self.outgoing_edges_constraints = pyo.Constraint(
            S, rule=lambda model, i, j:
                pyo.quicksum(x[(i,j), w] for w in S if ((i,j), w) in E) == 0 if N[len(K)] == (i,j) else
                pyo.quicksum(x[(i,j), w] for w in S if ((i,j), w) in E) == 1
        )
        self.incoming_edges_constraints = pyo.Constraint(
            S, rule=lambda model, i, j:
                pyo.quicksum(x[s, (i,j)] for s in S if (s, (i,j)) in E) == 0 if N[1] == (i,j) else
                pyo.quicksum(x[s, (i,j)] for s in S if (s, (i,j)) in E) == 1
        )
        self.wall_constraints = pyo.Constraint(
            W, rule=lambda model, i, j, r, s: x[i,j,r,s] + x[r,s,i,j] == 0
        )
        M = m * n # Big M
        self.subroute_elimination_constraints = pyo.Constraint(
            E, rule=lambda model, i, j, r, s: u[r,s] >= u[i,j] + 1 - M * (1 - x[i,j,r,s])
        )
        self.ordinal_position_constraints = pyo.Constraint(
            K, rule= lambda model, k:
                u[N[k]] == 1 if k == 1 else
                u[N[k]] == M if k == len(N) else
                u[N[k]] >= u[N[k-1]] + 1
        )
