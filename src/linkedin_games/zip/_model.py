import pyomo.environ as pyo


class ZipModel(pyo.ConcreteModel):
    """Linear Optimization Model for Zip game"""
    def __init__(self,
            board_dims:tuple[int, int],
            numbered_squares:dict[tuple[int, int]: int],
            walls:tuple[tuple[int, int], tuple[int, int]] | None):
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
        E = self.E = pyo.Set(initialize=lambda model: # Edges
            [((i, j), (i+1, j)) for i in I for j in J if i+1 in I] +
            [((i, j), (i-1, j)) for i in I for j in J if i-1 in I] +
            [((i, j), (i, j+1)) for i in I for j in J if j+1 in J] +
            [((i, j), (i, j-1)) for i in I for j in J if j-1 in J]
        )
        K = self.K = pyo.Set(initialize=numbered_squares.keys(), dimen=2) # Numbered Squares
        W = self.W = pyo.Set(initialize=walls) # Walls
        
        # DECISION VARIABLES
        x = self.x = pyo.Var(E, within=pyo.Binary, initialize=0)
        u = self.u = pyo.Var(S, within=pyo.NonNegativeReals)

        # PARAMETERS
        k = self.k = pyo.Param(S, initialize=numbered_squares, within=pyo.NonNegativeIntegers, default=0)

        # OBJECTIVE FUNCTION
        self.obj = pyo.Objective(expr=0) # feasibility problem
    
        # CONSTRAINTS
        self.outgoing_edges_constraints = pyo.Constraint(
            S, rule=lambda model, i, j:
                sum(x[(i,j),w] for w in S if ((i,j),w) in E) == 1 if k[i,j] != len(K)
                else sum(x[(i,j),w] for w in S if ((i,j),w) in E) == 0
        )
        self.incoming_edges_constraints = pyo.Constraint(
            S, rule=lambda model, i, j:
                sum(x[s,(i,j)] for s in S if (s,(i,j)) in E) == 1 if k[i,j] != 1
                else sum(x[s,(i,j)] for s in S if (s,(i,j)) in E) == 0
        )
        self.wall_constraints = pyo.Constraint(
            W, rule=lambda model, i, j, r, s: x[i,j,r,s] + x[r,s,i,j] == 0
        )
        M = m * n # Big M
        self.subroute_elimination_constraints = pyo.Constraint(
            E, rule=lambda model, i, j, r, s:
                u[r, s] >= u[i, j] + 1 - M * (1 - x[i, j, r, s])
        )
        self.first_square_position_constraint = pyo.Constraint(
            K, rule= lambda model, i, j:
                u[i,j] == 1 if k[i,j] == 1 else pyo.Constraint.Skip
        )
        self.ordinal_position_constraints = pyo.Constraint(
            K, K, rule= lambda model, i, j, r, s:
                u[i,j] >= u[r,s] + 1 if k[i,j] == k[r,s] + 1 else pyo.Constraint.Skip
        )
        self.last_square_position_constraint = pyo.Constraint(
            K, rule= lambda model, i, j: u[i,j] == M if k[i,j] == len(K) else pyo.Constraint.Skip
        )
