from pprint import pprint

from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

try:
    from ..gameboard import GameBoard
except ImportError:  # pragma: no cover - allows running the module as a script
    from linkedin_games.gameboard import GameBoard


class Tango(GameBoard):

    def __init__(
            self,
            board_dims:tuple[int, int],
            like_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None,
            opp_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None,
            filled_squares:dict[tuple[int, int]: int] | None
            ) -> None:
        super().__init__(board_dims)
        self.like_pairs = like_pairs
        self.opp_pairs = opp_pairs
        self.filled_squares = filled_squares


    def __hash__(self) -> int:
        return hash((self._dims, self._like_pairs, self._opp_pairs, self._filled_squares))


    @staticmethod
    def __manhathan_distance(squares:tuple[tuple[int, int], tuple[int, int]]) -> int:
        x1 = squares[0][0]
        x2 = squares[1][0]
        y1 = squares[0][1]
        y2 = squares[1][1]
        return abs(x1 - x2) + abs(y1 - y2)


    @property
    def like_pairs(self) -> tuple[tuple[tuple[int, int], tuple[int, int]]] | None:
        return self._like_pairs
    
    @like_pairs.setter
    def like_pairs(self, value:tuple[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
        if value is None:
            self._like_pairs = value
            return None

        invalid_items = [pair for pair in value if not isinstance(pair, tuple) or len(pair) != 2]
        if invalid_items:
            msg = (
                "like_pairs must be a collection of pairs of tuples. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [square for pair in value for square in pair if not isinstance(square, tuple)]
        if invalid_items:
            msg = (
                "Squares in pair must be tuples of positive integers. "
                f"Got the following invalid squares: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [square for pair in value for square in pair for coord in square if not isinstance(coord, int) or coord < 1]
        if invalid_items:
            msg = (
                "Coordinates must be positive integers. "
                f"Got the following invalid squares: {invalid_items!r}."
            )
            raise ValueError(msg)

        invalid_items = [pair for pair in value if Tango.__manhathan_distance(pair) != 1]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)
        
        if not isinstance(value, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, "
                "like_pairs should be a tuple. "
                f"Got a {type(value).__name__} instead."
            ))
            self._like_pairs = tuple(value)
        else:
            self._like_pairs = value
        
        self._stale = True


    @property
    def opp_pairs(self) -> tuple[tuple[tuple[int, int], tuple[int, int]]] | None:
        return self._opp_pairs
    
    @opp_pairs.setter
    def opp_pairs(self, value:tuple[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
        if value is None:
            self._opp_pairs = value
            return None

        invalid_items = [pair for pair in value if not isinstance(pair, tuple) or len(pair) != 2]
        if invalid_items:
            msg = (
                "opp_pairs must be a collection of pairs of tuples. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [square for pair in value for square in pair if not isinstance(square, tuple)]
        if invalid_items:
            msg = (
                "Squares in pair must be tuples of positive integers. "
                f"Got the following invalid squares: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [square for pair in value for square in pair for coord in square if not isinstance(coord, int) or coord < 1]
        if invalid_items:
            msg = (
                "Coordinates must be positive integers. "
                f"Got the following invalid squares: {invalid_items!r}."
            )
            raise ValueError(msg)

        invalid_items = [pair for pair in value if Tango.__manhathan_distance(pair) != 1]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)
        
        if not isinstance(value, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, "
                "opp_pairs should be a tuple. "
                f"Got a {type(value).__name__} instead."
            ))
            self._opp_pairs = tuple(value)
        else:
            self._opp_pairs = value
        
        self._stale = True


    @property
    def filled_squares(self) -> dict[tuple[int, int]: int]:
        return self._filled_squares
    
    @filled_squares.setter
    def filled_squares(self, values:dict[tuple[int, int]: int]) -> None:

        if len(values) > len(self):
            msg = (
                "The number of filled squares exceeds the amount of board squares! "
                f"Got {len(values)} filled squares."
            )
            raise ValueError(msg)

        if not isinstance(values, dict):
            msg = f"filled_squares must be a dictionary. Got a {type(values).__name__} type instead."
            raise ValueError(msg)

        invalid_items = {square: value for square, value in values.items() if value != 1 and value != 0}
        if invalid_items:
            msg = (
                "The square values must be of binary type. "
                f"Got the following invalid values: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        self._filled_squares = {square: (1 if value else 0) for square, value in values.items()}


    def __build__model(self) -> None:
        model = pyo.ConcreteModel()

        # BOARD DIMENSIONS
        m, n = self._board_dims
        model.m = pyo.Param(initialize=m, within=pyo.PositiveIntegers)
        model.n = pyo.Param(initialize=n, within=pyo.PositiveIntegers)

        # RANGE SETS
        I = model.I = pyo.RangeSet(n) # Rows
        J = model.J = pyo.RangeSet(m) # Columns

        # COMPOSITE SETS
        S = model.S = pyo.Set(initialize=lambda model: [(i, j) for i in I for j in J]) # Board Squares
        L = model.L = pyo.Set(initialize=self._like_pairs)
        O = model.O = pyo.Set(initialize=self._opp_pairs)
        K = model.K = pyo.Set(initialize=self._filled_squares.keys(), dimen=2)

        # DECISION VARIABLES
        x = model.x = pyo.Var(S, within=pyo.Binary)

        # PARAMETERS
        k = model.k = pyo.Param(K, initialize=self._filled_squares, within=pyo.Binary) # Filled values

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0) # feasibility problem

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


    def solve(self, solver:str="gurobi", verbose:bool=False):

        if self._stale or self.model is None:
            self.__build__model()

        result = pyo.SolverFactory(solver).solve(self.model)

        is_model_solved = (
            result.Solver.status == SolverStatus.ok # Checks if solver is finished with normal termination.
            and (
                result.Solver.termination_condition == TerminationCondition.optimal # Checks if solver is finished with optimal solution...
                or result.Solver.termination_condition == TerminationCondition.feasible # ... or with feasible solution.
            ))

        if is_model_solved:

            print("Tango solved successfully!")
            nx.set_node_attributes(
                self._board,
                name="value",
                values={(i-1, j-1): int(pyo.value(self.model.x[i,j])) for i, j in self.model.S}
            )

            if verbose:
                print("Tango solution:")
                pprint(self.board_squares)

        else:
            print("No feasible solution was found!")
            print(result.Solver)


    def show(self):

        if self._stale or self.model is None:
            self.__build__model()
        
        plt.figure(figsize=(3.4, 3.4))
        
        pos = {(i, j): (j, -i) for i, j in self.board.nodes()}

        nx.draw(
            self.board,
            pos= pos,
            with_labels= True,
            labels= nx.get_node_attributes(self.board, "value"),
            node_size= 1000,
            node_color= ["#EEEAE7" if (i+1,j+1) in self.filled_squares else "white" for (i, j) in self.board.nodes()],
            node_shape="s",
            edgecolors="#EEEAE7",
            linewidths= 1,
            width= 0,
            edgelist = [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.model.O] + [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.model.L
            ]
        )

        nx.draw_networkx_edge_labels(
            self._board,
            pos= pos,
            edge_labels= {
                ((i-1, j-1), (r-1,s-1)): "×" for i,j,r,s in self.model.O} | {
                ((i-1, j-1), (r-1,s-1)): "=" for i,j,r,s in self.model.L
            },
            font_color="#887658"
        )
        plt.show()


if __name__ == "__main__":

    # Solving Tango No. 151

    # like (=) pairs, each element is ((i,j),(r,s))
    like_pairs = (
        ((2, 3), (2, 4)),
        ((2, 1), (3, 1)),
        ((2, 3), (3, 3)),
        ((2, 6), (3, 6)),
        ((4, 1), (4, 2)),
        ((6, 3), (6, 4)),
    )

    # opposite (X) pairs
    opp_pairs = (
        ((2, 4), (3, 4)),
        ((3, 1), (4, 1)),
        ((3, 3), (3, 4)),
        ((3, 6), (4, 6)),
        ((4, 5), (4, 6)),
    )

    # already filled squares: (i,j) -> kij
    filled_squares = {
        (1, 2): 1,
        (1, 5): 1,
        (5, 2): 0,
        (5, 5): 1,
    }

    tango = Tango((6,6), like_pairs, opp_pairs, filled_squares)
    tango.solve(verbose=True)
    tango.show()
