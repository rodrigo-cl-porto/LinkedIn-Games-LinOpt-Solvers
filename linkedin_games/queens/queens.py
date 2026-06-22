from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from region import Region


class Queens():

    def __init__(self, board_dims:tuple[int, int], regions:dict[str: list[tuple[int, int]]]) -> None:
        self.board_dims = board_dims
        self.regions = regions
        self._model: pyo.ConcreteModel | None = None
        self._crowns = set()
        self._stale = True # This tells if the model is obsolete or not.


    def _build_model(self):
        model = pyo.ConcreteModel()

        # PARAMETERS
        m, n = self.board_dims
        model.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        model.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGES
        I = model.I = pyo.RangeSet(n) # Rows
        J = model.J = pyo.RangeSet(m) # Columns
        K = model.Colors = pyo.Set(initialize={region.name for region in self.regions}) # Regions

        # COMPOSITE SETS
        S = model.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Squares
        R = model.R = pyo.Set(K, initialize=self.regions, dimen=2) # Regions
        D = model.D = pyo.Set(initialize=lambda model: [
            ((i, j), (i+1, j+1)) for (i, j) in S if (i+1, j+1) in S] + [
            ((i, j), (i+1, j-1)) for (i, j) in S if (i+1, j-1) in S
        ]) # Diagonals

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0)

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
        self._stale = False


    @property
    def board_dims(self) -> tuple[int, int]:
        return self._board_dims

    @board_dims.setter
    def board_dims(self, value:tuple[int, int] = (1, 1)) -> None:

        if not isinstance(value, tuple):
            msg = f"board_dims must be a tuple, got {value!r}"
            raise ValueError(msg)
        
        if len(value) != 2:
            msg = f"board_dims must be a pair (m,n), got {value!r}"
            raise ValueError(msg)
        
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in value):
            msg = f"board_dims entries must be integers, got {value!r}"
            raise ValueError(msg)
        
        if any(x < 1 for x in value):
            msg = f"board_dims entries must be positive, got {value!r}"
            raise ValueError(msg)

        self._board_dims = value
        self._stale = True


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
        
        if len(value) != len({region.color for region in value}):
            msg = "There must not be two regions with the same color."
            raise ValueError(msg)

        if sum(len(region.squares) for region in value) != len(self):
            msg = "The regions must be a partition of the board game."
            raise ValueError(msg)

        self._regions = value
        self._stale = True


    @property
    def crowns(self) -> set[tuple[int, int]]:
        return self._crowns


    def __len__(self) -> int:
        m, n = self._board_dims
        return m * n


    def solve(self, verbose:bool=False) -> None:

        if self._stale or self._model is None:
            self._build_model()
        
        # Optmization result
        result = pyo.SolverFactory("gurobi").solve(self._model)

        if result.Solver.status == SolverStatus.ok and result.Solver.termination_condition == TerminationCondition.feasible:
            print("Queens solved successfully!")
            self._crowns = set((i,j) for i in self._model.I for j in self._model.J if round(self._model.x[i,j].value, 0) == 1)
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
        
        squares = [(i-1, j-1) for (i, j) in sorted(list(self._model.S))]

        color_map = [{(i-1, j-1): region for (i,j) in squares} for region, squares in regions.items()]
        color_map = {square: region for d in color_map for square, region in d.items()}
        color_map = [color_map[square] for square in squares]
        
        hex_map = {
            "purple": "#BBA3E1",
            "orange": "#FFC794",
            "blue": "#94BEFF",
            "green": "#B3DF9E",
            "gray": "#E0E0E0",
            "red": "#FF7B61",
            "yellow": "#E6F388"
        }

        color_map = [hex_map[color] for color in color_map]
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
    regions = set(
        Region("Purple", {(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,6), (2,7), (3,6), (3,7), (4,6), (4,7), (5,7), (6,7), (7,7)}, "#BBA3E1"),
        Region("Orange", {(2,1), (2,2), (2,3), (2,4), (3,1), (4,1), (4,2), (5,1), (5,2), (6,1), (6,2), (6,4), (6,5), (6,6), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6)}, "#FFC794"),
        Region("Blue", {(2,5), (3,5)}, "#94BEFF"),
        Region("Green", {(3,2), (3,3)}, "#B3DF9E"),
        Region("Gray", {(3,4), (4,3), (4,4), (4,5), (5,4)}, "#E0E0E0"),
        Region("Red", {(5,3), (6,3)}, "#FF7B61"),
        Region("Yellow", {(5,5), (5,6)}, "#E6F388"),
    )

    queens = Queens((7,7), regions)
    queens.solve()
    queens.show()
