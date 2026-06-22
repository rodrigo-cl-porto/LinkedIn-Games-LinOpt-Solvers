from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from rectangle import Rectangle, RecType


class Patches:

    def __init__(self, board_dims: tuple[int, int], rectangles: dict[str, Rectangle]):
        self.board_dims = board_dims
        self.rectangles = rectangles
        self._model: pyo.ConcreteModel | None = None
        self._stale = True # This tells if the model is obsolete or not.


    @property
    def board_dims(self) -> tuple[int, int]:
        return self._board_dims

    @board_dims.setter
    def board_dims(self, value: tuple[int, int] = (1, 1)) -> None:

        if not isinstance(value, tuple[int, int]):
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
    def rectangles(self) -> dict[str, Rectangle]:
        return self._rectangles

    @rectangles.setter
    def rectangles(self, value: dict[str, Rectangle]) -> None:

        if not isinstance(value, dict):
            msg = "Rectangles must be a dict keyed by rectangle names."
            raise ValueError(msg)
        
        if len(value) < 1:
            msg = "The dictionary of rectangles cannot be empty!"
            raise ValueError(msg)

        self._rectangles = value
        self._stale = True


    def __len__(self) -> int:
        m, n = self._board_dims
        return m * n


    def _build_model(self) -> None:
        m, n = self._board_dims
        rectangles = self._rectangles

        model = pyo.ConcreteModel()

        # INDEX SETS
        I = model.I = pyo.RangeSet(m)  # Rows
        J = model.J = pyo.RangeSet(n)  # Columns
        K = model.K = pyo.Set(initialize=list(rectangles.keys())) # Rectangles

        # COMPOSITE SETS
        S = model.S = pyo.Set(initialize=[(i, j) for i in I for j in J])
        # T is a set of triples (i,j,k) indicating tip square (i,j) for rectangle k
        T = model.T = pyo.Set(initialize=[(rect.tip_square[0], rect.tip_square[1], key) for key, rect in rectangles.items()])
        V = model.V = pyo.Set(initialize=[key for key, rect in rectangles.items() if rect.tip_type == RecType.VERTICAL])
        H = model.H = pyo.Set(initialize=[key for key, rect in rectangles.items() if rect.tip_type == RecType.HORIZONTAL])
        Q = model.Q = pyo.Set(initialize=[key for key, rect in rectangles.items() if rect.tip_type == RecType.SQUARE])
        A = model.A = pyo.Set(initialize=[key for key, rect in rectangles.items() if rect.tip_area is not None])

        # DECISION VARIABLES
        x = model.x = pyo.Var(I, J, K, domain=pyo.Binary)
        c = model.c = pyo.Var(K, domain=pyo.PositiveIntegers) # Column index of first cell of rectangle k
        r = model.r = pyo.Var(K, domain=pyo.PositiveIntegers) # Row index of first cell of rectangle k
        w = model.w = pyo.Var(K, domain=pyo.PositiveIntegers) # Width of rectangle k
        h = model.h = pyo.Var(K, domain=pyo.PositiveIntegers) # Height of rectangle k

        # PARAMETERS: tip area for those rectangles that specify it
        a = model.a = pyo.Param(
            K,
            initialize= {key: rect.tip_area for key, rect in rectangles.items() if rect.tip_area is not None}
        )

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=sum(w[k] + h[k] for k in K), sense=pyo.minimize)

        # CONSTRAINTS
        # Non overlapping rectangles
        model.unique_rectangle_per_square_constraints = pyo.Constraint(
            S,
            rule=lambda model, i, j: sum(x[i, j, k] for k in K) == 1
        )

        # Rectangle inside board
        model.last_row_position_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: r[k] + h[k] - 1 <= m
        )
        model.last_column_position_constraints = pyo.Constraint(
            K,
            rule=lambda model, k: c[k] + w[k] - 1 <= n
        )

        # Coverage constraints (if x[i,j,k]=1 then row/col must be within r..r+h-1 etc.)
        model.row_lower_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: r[k] - i <= m * (1 - x[i, j, k])
        )
        model.row_upper_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: i - (r[k] + h[k] - 1) <= m * (1 - x[i, j, k])
        )
        model.column_lower_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: c[k] - j <= n * (1 - x[i, j, k])
        )
        model.column_upper_bound_coverage_constraints = pyo.Constraint(
            I, J, K,
            rule=lambda model, i, j, k: j - (c[k] + w[k] - 1) <= n * (1 - x[i, j, k])
        )

        # Tip Constraints

        # Tip square
        model.tip_square_constraints = pyo.Constraint(
            T,
            rule=lambda model, i, j, k: x[i, j, k] == 1
        )

        # Tip area
        model.tip_area_constraints = pyo.Constraint(
            A,
            rule=lambda model, k: sum(x[i, j, k] for (i, j) in S) == a[k]
        )

        # Orientation constraints
        model.vertical_rectangle_constraints = pyo.Constraint(
            V,
            rule=lambda model, k: w[k] <= h[k] - 1
        )
        model.horizontal_rectangle_constraints = pyo.Constraint(
            H,
            rule=lambda model, k: w[k] >= h[k] + 1
        )
        model.square_rectangle_constraints = pyo.Constraint(
            Q,
            rule=lambda model, k: w[k] == h[k]
        )

        # Attach model
        self._model = model
        self._stale = False


    def solve(self, verbose:bool = False) -> None:

        if self._stale or self._model is None:
            self._build_model()

        result = pyo.SolverFactory("highs").solve(self._model)

        if result.Solver.status == SolverStatus.ok and result.Solver.termination_condition == TerminationCondition.optimal:
            print("Optimal solution found!")
            for k in self._model.K:
                rect = self._rectangles[k]
                rect.x = int(round(pyo.value(self._model.c[k]), 0))
                rect.y = int(round(pyo.value(self._model.r[k]), 0))
                rect.width = int(round(pyo.value(self._model.w[k]), 0))
                rect.height = int(round(pyo.value(self._model.h[k]), 0))
                if verbose:
                    print(f"{k}: {repr(rect)}")
        else:
            print("It was not possible to find a feasible solution for the game.")
            print(result.Solver)


    def show(self) -> None:

        if self._stale or self._model is None:
            self._build_model()

        m, n = self._board_dims
        G = nx.grid_2d_graph(m, n)
        plt.figure(figsize=(3, 3))

        # compute color per node (i,j) by looking at x[i,j,k]
        color_map = []
        for (i, j) in G.nodes():
            color = None
            for k in self._model.K:
                if round(pyo.value(self._model.x[i+1, j+1, k]), 0) == 1:
                    color = self._rectangles[k].color
                    break
            color_map.append(color if color is not None else "#000000")

        nx.draw(
            G,
            pos={(i, j): (j, -i) for (i, j) in G.nodes()},
            node_size=1100,
            node_shape="s",
            node_color=color_map,
            width=0,
        )
        plt.show()


if __name__ == "__main__":

    # Solving Patches No. 16
    rectangles = {
        "yellow":  Rectangle((1, 2), RecType.ANY,      2, "#846A0B"),
        "teal":    Rectangle((1, 4), RecType.ANY,      6, "#096B78"),
        "purple":  Rectangle((2, 6), RecType.ANY,      2, "#5A3DB1"),
        "green":   Rectangle((3, 1), RecType.ANY,      6, "#0A7541"),
        "orange":  Rectangle((3, 3), RecType.VERTICAL, 2, "#EF6C00"),
        "red":     Rectangle((4, 4), RecType.SQUARE,   4, "#E30102"),
        "blue":    Rectangle((4, 6), RecType.ANY,      2, "#097BB1"),
        "magenta": Rectangle((5, 1), RecType.ANY,      2, "#A01E4E"),
        "brick":   Rectangle((6, 3), RecType.ANY,      6, "#9B3C1C"),
        "brown":   Rectangle((6, 5), RecType.ANY,      4, "#503B36")
    }

    patches = Patches((6, 6), rectangles)
    patches.solve(verbose=True)
    patches.show()
