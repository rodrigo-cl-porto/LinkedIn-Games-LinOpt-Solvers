from pprint import pprint

from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..gameboard import GameBoard


class Zip(GameBoard):

    def __init__(
            self,
            board_dims: tuple[int, int],
            numbered_squares: dict[tuple[int, int]: int] | list[tuple[int, int]],
            walls: tuple[tuple[int, int]] | None
        ):
        super().__init__(board_dims)
        self.numbered_squares = numbered_squares
        self.walls = walls
        self.__build_board()


    def __hash__(self):
        return hash((self._board_dims, self._numbered_squares, self._walls))


    def __build_board(self):
        super()._build_board()
        nx.set_node_attributes(self._board, name="value", values=self._numbered_squares)


    def _build_model(self):
        model = pyo.ConcreteModel()

        # BOARD DIMENSIONS
        m, n = model._board_dims
        model.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        model.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)
        
        M = m * n

        # RANGE SETS
        I = model.I = pyo.RangeSet(m) # Rows
        J = model.J = pyo.RangeSet(n) # Columns

        # COMPOSITE SETS
        V = model.V = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Nodes
        E = model.E = pyo.Set(initialize=lambda model: [
            ((i, j), (i+1, j)) for i in I for j in J if i+1 in I] + [
            ((i, j), (i-1, j)) for i in I for j in J if i-1 in I] + [
            ((i, j), (i, j+1)) for i in I for j in J if j+1 in J] + [
            ((i, j), (i, j-1)) for i in I for j in J if j-1 in J]
        ) # Edges
        K = model.K = pyo.Set(initialize=model._numbered_squares.keys(), dimen=2)
        W = model.W = pyo.Set(initialize=model._walls)
        
        # DECISION VARIABLES
        x = model.x = pyo.Var(E, within=pyo.Binary, initialize=0)
        u = model.u = pyo.Var(V, within=pyo.NonNegativeReals)

        # PARAMETERS
        k = model.k = pyo.Param(V, initialize=self._numbered_squares, default=0, within=pyo.NonNegativeIntegers)

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0) # feasibility problem
    
        # CONSTRAINTS
        model.outgoing_edges_constraints = pyo.Constraint(
            V,
            rule=lambda model, i, j: \
                sum(x[(i,j),w] for w in V if ((i,j),w) in E) == 1 if k[i,j] != len(K) else \
                sum(x[(i,j),w] for w in V if ((i,j),w) in E) == 0
        )
        
        model.incoming_edges_constraints = pyo.Constraint(
            V,
            rule=lambda model, i, j: \
                sum(x[v,(i,j)] for v in V if (v,(i,j)) in E) == 1 if k[i,j] != 1 else \
                sum(x[v,(i,j)] for v in V if (v,(i,j)) in E) == 0
        )
    
        if W is not None:
            model.wall_constraints = pyo.Constraint(
                W,
                rule=lambda model, i, j, r, s: x[i,j,r,s] + x[r,s,i,j] == 0
            )

        model.subroute_elimination_constraints = pyo.Constraint(
            E,
            rule=lambda model, i, j, r, s: u[r,s] >= u[i,j] + 1 - M*(1 - x[i,j,r,s])
        )
        
        model.first_square_position_constraint = pyo.Constraint(
            K,
            rule= lambda model, i, j: u[i,j] == 1 if k[i,j] == 1 else pyo.Constraint.Skip
        )
        
        model.ordinal_position_constraints = pyo.Constraint(
            K, K,
            rule= lambda model, i, j, r, s: u[i,j] >= u[r,s] + 1 if k[i,j] == k[r,s] + 1 else pyo.Constraint.Skip
        )
        
        model.last_square_position_constraint = pyo.Constraint(
            K,
            rule= lambda model, i, j: u[i,j] == M if k[i,j] == len(K) else pyo.Constraint.Skip
        )

        # Attach model
        self._model = model
        self._stale = False


    @property
    def numbered_squares(self):
        return self._numbered_squares
    
    @numbered_squares.setter
    def numbered_squares(self, values) -> None:

        if len(values) > len(self):
            msg = (
                "The number of numbered squares exceeds the amount of board squares! "
                f"Got {len(values)} numbered squares."
            )
            raise ValueError(msg)
        
        if len(values) < 2:
            msg = (
                "The quantity of numbered squares is too small for the game! "
                f"Got a total of {len(values)} numbered squares."
            )
            raise ValueError(msg)

        if isinstance(values, (list, tuple)):
            print((
                "WARNING: The numbered squares should be a dictionary mapping (i,j) coordinates to their respective numbers. "
                f"Got a {type(values).__name__} instead."
            ))
            self._numbered_squares = {square: index for index, square in enumerate(values)}
        elif not isinstance(numbered_squares, dict):
            msg = "The numbered squares must be a dictionary."
            raise ValueError(msg)
        else:
            self._numbered_squares = values

        self._stale = True


    def solve(self, verbose:bool=False):

        if self._stale or self._model is None:
            self._build_model()

        result = pyo.SolverFactory("highs").solve(self)

        if (result.Solver.status == SolverStatus.ok
            and (
                result.Solver.termination_condition == TerminationCondition.feasible
                or result.Solver.termination_condition == TerminationCondition.optimal
            )):
            print("Zip solved successfully!")
            nx.set_edge_attributes(
                self._board,
                name="value",
                values={((i-1, j-1), (r-1, s-1)): round(pyo.value(self._model.x[i,j,r,s])) for i, j, r, s in self._model.E}
            )

            if verbose:
                pprint(self.board_edges)

        else:
            print("No feasible solution was found!")
            print(result.Solver)


    def show(self):

        if self._stale or self._model is None:
            self._build_model()

        plt.figure(figsize=(3.4, 3.4))
        
        nx.draw(
            self._board,
            pos= {(i,j): (j,-i) for i, j in self._board.nodes()},
            with_labels= True,
            labels= {(i-1, j-1): self._model.k[i,j] for (i,j) in self._model.K},
            arrows=False,
            node_shape="o", # round nodes
            node_size= 1000,
            node_color= ["white" if (i+1,j+1) in self._model.K else "#EE5F12" for (i,j) in self._board.nodes()],
            edge_color= "#EE5F12",
            edgecolors='#EE5F12',
            linewidths= 3,
            width= 35,
            edgelist= [((i-1, j-1), (r-1, s-1)) for i,j,r,s in self._model.E if round(self._model.x[i,j,r,s].value) == 1]
        )
        plt.show()


if __name__ == "__main__":

    # Zip No. 166
    
    numbered_squares = {
        (1,1):  9,
        (1,2): 10,
        (1,3): 11,
        (2,1):  8,
        (2,4): 13,
        (3,1):  7,
        (3,4): 14,
        (3,5): 12,
        (4,2):  6,
        (4,3): 15,
        (4,6): 16,
        (5,3):  5,
        (5,6):  3,
        (6,4):  4,
        (6,5):  1,
        (6,6):  2
    }

    zip = Zip((6,6), numbered_squares)
    zip.solve()
    zip.show()