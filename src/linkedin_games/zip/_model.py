from ..core._taxicab_distance_mixin import TaxicabDistanceMixin
import pyomo.environ as pyo


class ZipModel(TaxicabDistanceMixin, pyo.ConcreteModel):
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

        # PARAMETERS
        m, n = board_dims
        M = m * n # Big M
        self.m = pyo.Param(initialize=m, domain=pyo.PositiveIntegers)
        self.n = pyo.Param(initialize=n, domain=pyo.PositiveIntegers)

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
        W = self.W = pyo.Set(initialize=walls, domain=E) # Walls
        N = self.N = pyo.Set(initialize=numbered_squares, domain=S)

        # DECISION VARIABLES
        x = self.x = pyo.Var(E, domain=pyo.Binary, initialize=0) # Decision to go from square (i,j) to (r,s)
        u = self.u = pyo.Var( # Visitiation order of a square (i, j)
            S, domain=pyo.PositiveIntegers, initialize=1, bounds=(1, M)
        ) 

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0) # feasibility problem

        # CONSTRAINTS

        ## Edge constraints
        neighbors = { # This dictionary is important to access all neighbors of a square quickly.
            (i, j): [
                (r, c) for r, c in [
                    (i-1, j),
                    (i+1, j),
                    (i, j-1),
                    (i, j+1)
                ] if (r, c) in S
            ] for (i, j) in S
        }
        self.outgoing_edges_constraints = pyo.Constraint(
            S, rule=lambda model, i, j:
                pyo.quicksum(x[(i,j), w] for w in neighbors[(i,j)]) == 0 if N[len(K)] == (i,j) else
                pyo.quicksum(x[(i,j), w] for w in neighbors[(i,j)]) == 1
        )
        self.incoming_edges_constraints = pyo.Constraint(
            S, rule=lambda model, i, j:
                pyo.quicksum(x[s, (i,j)] for s in neighbors[(i,j)]) == 0 if N[1] == (i,j) else
                pyo.quicksum(x[s, (i,j)] for s in neighbors[(i,j)]) == 1
        )

        ## Blocked paths constraints
        self.wall_constraints = pyo.Constraint(
            W, rule=lambda model, i, j, r, s: x[i,j,r,s] + x[r,s,i,j] == 0
        )

        # Miller-Tucker-Zemlin constraints with lifting
        self.subroute_elimination_constraints = pyo.Constraint(
            E, rule=lambda model, i, j, r, s: u[r,s] >= u[i,j] + 1 - M * (1 - x[i,j,r,s]) + (M - 2) * x[r,s,i,j]
        )

        ## Visitation order constraints
        self.visitation_order_constraints = pyo.Constraint(
            K, rule= lambda model, k:
                u[N[k]] == 1 if k == 1 else
                u[N[k]] == M if k == len(N) else
                u[N[k]] >= u[N[k-1]] + self._taxicab_distance(N[k], N[k-1])
        )
