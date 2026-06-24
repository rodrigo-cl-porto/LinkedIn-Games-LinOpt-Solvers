from pprint import pprint

from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from linkedin_games.gameboard import GameBoard
from region import Region


class Queens(GameBoard):

    """
    A class representing a Queens board game with colored regions.
    """

    def __init__(self, board_dims:tuple[int, int], regions:set[Region]) -> None:
        super().__init__(board_dims)
        self.regions = regions


    def __hash__(self):
        return hash((self._board_dims, self._regions))


    @property
    def regions(self) -> set[Region]:
        return self._regions

    @regions.setter
    def regions(self, value:set[Region]) -> None:

        if not isinstance(value, set):
            msg = "Regions must be a set of Region classes."
            raise TypeError(msg)
        
        if len(value) < 1:
            msg = "The set of Regions cannot be empty!"
            raise ValueError(msg)
        
        if any(not isinstance(region, Region) for region in value):
            msg = "All elements of the set must be Region classes."
            raise TypeError(msg)
        
        if len(value) != len({region.color for region in value}):
            msg = "There must not be two regions with the same color."
            raise ValueError(msg)
        
        all_region_squares = [square for region in value for square in region.squares]
        overlapping_squares = {square for square in all_region_squares if all_region_squares.count(square) > 1}
        if overlapping_squares:
            msg = (
                "The regions must not overlap each other.\n"
                f"The following squares are in more than one region: {overlapping_squares}"
            )
            raise ValueError(msg)

        all_region_squares = set(all_region_squares)
        if all_region_squares != self.board_squares:

            if len(all_region_squares) > len(self):
                squares_not_in_board = all_region_squares - self.board_squares
                msg = (
                    "The regions must cover the entire board and must not go beyond the board's boundaries. "
                    f"The following squares are outside the board: {squares_not_in_board!r}"
                )
                raise ValueError(msg)
            
            if len(all_region_squares) < len(self):
                missing_squares = self.board_squares - all_region_squares
                msg = (
                    "The regions must cover the entire board and must not go beyond the board's boundaries. "
                    f"The following board squares are not in any region: {missing_squares!r}"
                )
                raise ValueError(msg)

        self._regions = value
        self._stale = True


    @property
    def crowns(self) -> tuple[tuple[int, int]]:
        return tuple(square for square, data in self._board.nodes(data=True) if data.get("value") == 1)


    def _build_model(self):
        model = pyo.ConcreteModel()

        # PARAMETERS
        m, n = self.board_dims
        model.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        model.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = model.I = pyo.RangeSet(n) # Rows
        J = model.J = pyo.RangeSet(m) # Columns
        K = model.K = pyo.Set(initialize=[region.color for region in self.regions]) # Regions

        # COMPOSITE SETS
        S = model.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        R = model.R = pyo.Set(K, initialize={region.color: region.squares for region in self.regions}, dimen=2) # Region Squares
        D = model.D = pyo.Set(initialize=lambda model: [
            ((i, j), (i+1, j+1)) for (i, j) in S if (i+1, j+1) in S] + [
            ((i, j), (i+1, j-1)) for (i, j) in S if (i+1, j-1) in S
        ]) # Diagonals

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0) # feasibility problem

        # DECISION VARIABLES
        x = model.x = pyo.Var(S, within=pyo.Binary, initialize=0)

        # CONSTRAINTS
        model.single_crown_per_row_constraints = pyo.Constraint(
            I,
            rule=lambda model, i: sum(x[i,j] for j in J) == 1
        )

        model.single_crown_per_column_constraints = pyo.Constraint(
            J,
            rule=lambda model, j: sum(x[i,j] for i in I) == 1
        )

        model.single_crown_per_region_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: sum(x[i,j] for (i,j) in R[k]) == 1
        )

        model.adjacent_squares_by_vertex_constraints = pyo.Constraint(
            D,
            rule=lambda model, i, j, r, s: x[i,j] + x[r,s] <= 1
        )

        # Attach model
        self._model = model
        self._stale = False # The model is now up to date.


    def solve(self, verbose:bool=False) -> None:

        if self._stale or self._model is None:
            self._build_model()
        
        result = pyo.SolverFactory("gurobi").solve(self._model)

        if (result.Solver.status == SolverStatus.ok
            and (
                result.Solver.termination_condition == TerminationCondition.feasible
                or result.Solver.termination_condition == TerminationCondition.optimal
            )):
            print("Queens solved successfully!")
            self._crowns = [(i,j) for i in self._model.I for j in self._model.J if round(self._model.x[i,j].value, 0) == 1]
            if verbose:
                print(self._crowns)
                
        else:
            print("No feasible solution was found!")
            if verbose:
                print(result.Solver)


    def show(self) -> None:

        if self._stale or self._model is None:
            self._build_model()

        m, n = self._board_dims
        G = nx.grid_2d_graph(m, n)
        plt.figure(figsize=(3.4, 3.4))

        color_map = {(i-1, j-1): region.color for region in self.regions for (i, j) in region.squares}
        color_map = [color_map[square] for square in sorted(color_map)]

        solution = [(i, j) for i in self._model.I for j in self._model.J if round(self._model.x[i,j].value, 0) == 1]

        nx.draw(
            G,
            pos= {(i, j): (j, -i) for i, j in G.nodes()},
            with_labels= True,
            labels= {(i-1, j-1): "O" for (i,j) in solution},
            node_size= 1000,
            node_color= color_map,
            node_shape="s",
            width=0
        )
        plt.show()


if __name__ == "__main__":

    # Solving Queens No. 307
    regions = {
        Region( # Purple
            color="#BBA3E1",
            squares={(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,6), (2,7), (3,6), (3,7), (4,6), (4,7), (5,7), (6,7), (7,7)}
        ),
        Region( # Orange
            color="#FFC794", 
            squares={(2,1), (2,2), (2,3), (2,4), (3,1), (4,1), (4,2), (5,1), (5,2), (6,1), (6,2), (6,4), (6,5), (6,6), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6)}
        ),
        Region( # Blue
            color="#94BEFF",
            squares={(2,5), (3,5)}
        ),
        Region( # Green
            color="#B3DF9E",
            squares={(3,2), (3,3)}
        ),
        Region( # Gray
            color="#E0E0E0",
            squares={(3,4), (4,3), (4,4), (4,5), (5,4)}
        ),
        Region( # Red
            color="#FF7B61",
            squares={(5,3), (6,3)}
        ),
        Region( # Yellow
            squares={(5,5), (5,6)},
            color="#E6F388"
        )
    }

    queens = Queens((7,7), regions)
    queens.solve(verbose=True)
    queens.show()
