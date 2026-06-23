from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo


class Tango:

    def __init__(self,
                board_dims:tuple[int, int],
                like_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None,
                opp_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None,
                filled_squares:dict[tuple[int, int]: bool] | None
                ) -> None:
        self.board_dims = board_dims
        self.like_pairs = like_pairs
        self.opp_pairs = opp_pairs
        self.filled_squares = filled_squares
        self._model: pyo.ConcreteModel | None = None
        self._stale: bool = True # This property indicates whether the model needs to be rebuilt due to changes in the game settings.
    

    def __hash__(self) -> int:
        return hash((self._board_dims, self._like_pairs, self._opp_pairs, self._filled_squares))


    def __len__(self) -> int:
        m, n = self._board_dims
        return m * n


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
    def like_pairs(self) -> set[tuple[tuple[int, int], tuple[int, int]]] | None:
        return self._like_pairs
    
    @like_pairs.setter
    def like_pairs(self, value:set[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        pass


    def _build_model(self) -> None:
        model = pyo.ConcreteModel()

        # BOARD DIMENSIONS
        m, n = self._board_dims
        model.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        model.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = model.I = pyo.RangeSet(n)
        J = model.J = pyo.RangeSet(m)

        # COMPOSITE SETS
        S = model.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        L = model.L = pyo.Set(initialize=like_pairs)
        O = model.O = pyo.Set(initialize=opp_pairs)
        K = model.K = pyo.Set(initialize=filled_squares.keys(), dimen=2)

        # DECISION VARIABLES
        x = model.x = pyo.Var(I, J, within=pyo.Binary)
    
        # PARAMETERS
        k = model.FilledValues = pyo.Param(K, initialize=filled_squares, within=pyo.Binary)

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0, sense=pyo.maximize)

        # CONSTRAINTS
        model.equal_moons_suns_per_row_constraints = pyo.Constraint(
            I,
            rule=lambda model, i: sum(x[i,j] for j in J) == n/2
        )

        model.equal_moons_suns_per_column_constraints = pyo.Constraint(
            J,
            rule=lambda model, j: sum(x[i,j] for i in I) == m/2
        )

        model.no_three_consecutive_moons_per_row_constraints = pyo.Constraint(
            I, pyo.RangeSet(n-2),
            rule=lambda model, i, j: x[i,j] + x[i,j+1] + x[i,j+2] <= 2
        )
    
        model.no_three_consecutive_suns_per_row_constraints = pyo.Constraint(
            I, pyo.RangeSet(n-2),
            rule=lambda model, i, j: x[i,j] + x[i,j+1] + x[i,j+2] >= 1
        )

        model.no_three_consecutive_moons_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(m-2), J,
            rule=lambda model, i, j: x[i,j] + x[i+1,j] + x[i+2,j] <= 2
        )
        
        model.no_three_consecutive_suns_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(m-2), J,
            rule=lambda model, i, j: x[i,j] + x[i+1,j] + x[i+2,j] >= 1
        )

        model.like_pairs_constraints = pyo.Constraint(
            L,
            rule=lambda model, i, j, r, s: x[i,j] - x[r,s] == 0
        )

        model.opposite_pairs_constraints = pyo.Constraint(
            O,
            rule=lambda model, i, j, r, s: x[i,j] + x[r,s] == 1
        )

        model.already_filled_squares_constraints = pyo.Constraint(
            K,
            rule=lambda model, i, j: x[i,j] == k[i,j]
        )

        # Attach model
        self._model = model
        self._stale = False

    
    def solve(self):

        result = pyo.SolverFactory("gurobi").solve(self)

        if result.Solver.status == SolverStatus.ok and result.Solver.termination_condition == TerminationCondition.feasible:
            print("Tango solved successfully!")
        else:
            print("No feasible solution was found!")
            print(result.Solver)

    
    def show(self):
        
        G = nx.grid_2d_graph(self.m, self.n)
        pos = {(i,j): (j, -i) for i, j in G.nodes()}
        
        plt.figure(figsize=(3.4, 3.4))
        
        nx.draw(
            G,
            pos= pos,
            with_labels= True,
            labels= {(i,j): int(self.x[i+1,j+1].value) for i, j in G.nodes()},
            node_size= 1000,
            node_color= ["#EEEAE7" if (i+1,j+1) in self.K else "white" for (i,j) in G.nodes()],
            node_shape="s",
            edgecolors="#EEEAE7",
            linewidths= 1,
            width= 0,
            edgelist = [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.O] + [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.L
            ]
        )
        nx.draw_networkx_edge_labels(
            G,
            pos= pos,
            edge_labels= {
                ((i-1, j-1), (r-1,s-1)): "×" for i,j,r,s in self.O} | {
                ((i-1, j-1), (r-1,s-1)): "=" for i,j,r,s in self.L
            },
            font_color="#887658"
        )
        plt.show()


if __name__ == "__main__":

    # like (=) pairs, each element is ((i,j),(r,s))
    like_pairs = {
        ((2, 3), (2, 4)),
        ((2, 1), (3, 1)),
        ((2, 3), (3, 3)),
        ((2, 6), (3, 6)),
        ((4, 1), (4, 2)),
        ((6, 3), (6, 4)),
    }

    # opposite (X) pairs
    opp_pairs = [
        ((2, 4), (3, 4)),
        ((3, 1), (4, 1)),
        ((3, 3), (3, 4)),
        ((3, 6), (4, 6)),
        ((4, 5), (4, 6)),
    ]

    # helper lists for the concrete instance (Tango #151)
    # already filled squares: (i,j) -> kij
    filled_squares = {
        (1, 2): 1,
        (1, 5): 1,
        (5, 2): 0,
        (5, 5): 1,
    }

    tango = Tango((6,6), like_pairs, opp_pairs, filled_squares)
    tango.solve()
    tango.show()