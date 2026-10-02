import pyomo.environ as pyo

from .._shared.optimization.modeler.opt_modeler import OptModeler
from .._shared.utils.taxicab_distance import TaxicabDistance
from ._game_grid import ZipGrid


class ZipOptModeler(OptModeler[ZipGrid]):

    def _set_range_sets(self) -> None:
        super()._set_range_sets()
        self._model.K = pyo.RangeSet(len(self._game.numbered_squares))

    def _set_composite_sets(self) -> None:
        super()._set_composite_sets()
        self._model.E = pyo.Set( # Edges
            initialize=lambda model:
                [((i,j), (i+1, j)) for i in model.I for j in model.J if i+1 in model.I] +
                [((i,j), (i-1, j)) for i in model.I for j in model.J if i-1 in model.I] +
                [((i,j), (i, j+1)) for i in model.I for j in model.J if j+1 in model.J] +
                [((i,j), (i, j-1)) for i in model.I for j in model.J if j-1 in model.J]
        )
        self._model.W = pyo.Set( # Walls
            initialize=self._game.walls,
            domain=self._model.E
        )
        self._model.N = pyo.Set(
            initialize=self._game.numbered_squares,
            domain=self._model.S
        )

    def _set_parameters(self) -> None:
        self._model.BigM = self._model.m * self._model.n

    def _set_decision_variables(self) -> None:
        self._model.x = pyo.Var( # Decision to go from square (i,j) to (r,s)
            self._model.E,
            domain=pyo.Binary,
            initialize=0
        )
        self._model.u = pyo.Var( # Visitiation order of a square (i, j)
            self._model.S,
            domain=pyo.PositiveIntegers,
            initialize=1,
            bounds=(1, self._model.BigM)
        )

    def _set_objective_function(self) -> None:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem

    def _set_constraints(self) -> None:
        self.__set_edge_constraints()
        self.__set_blocked_path_contraints()
        self.__set_subroute_elimination_constraints()
        self.__set_visitation_order_constraints()

    def __set_edge_constraints(self) -> None:
        neighbors = { # This dictionary is important to access all neighbors of a square quickly.
            (i, j): [
                (r, c) for r, c in [
                    (i-1, j),
                    (i+1, j),
                    (i, j-1),
                    (i, j+1)
                ] if (r, c) in self._model.S
            ]
            for (i, j) in self._model.S
        }
        self._model.outgoing_edges_constraints = pyo.Constraint(
            self._model.S,
            rule=lambda model, i, j:
                pyo.quicksum(model.x[(i,j), w] for w in neighbors[(i,j)]) == 0 if model.N.at(len(model.K)) == (i,j) else
                pyo.quicksum(model.x[(i,j), w] for w in neighbors[(i,j)]) == 1
        )
        self._model.incoming_edges_constraints = pyo.Constraint(
            self._model.S,
            rule=lambda model, i, j:
                pyo.quicksum(model.x[s, (i,j)] for s in neighbors[(i,j)]) == 0 if model.N.at(1) == (i,j) else
                pyo.quicksum(model.x[s, (i,j)] for s in neighbors[(i,j)]) == 1
        )

    def __set_blocked_path_contraints(self) -> None:
        self._model.wall_constraints = pyo.Constraint(
            self._model.W,
            rule=lambda model, i, j, r, s: model.x[i,j,r,s] + model.x[r,s,i,j] == 0
        )

    def __set_subroute_elimination_constraints(self) -> None:
        self._model.miller_tucker_zemlin_constraints = pyo.Constraint(
            self._model.E,
            rule=lambda model, i, j, r, s:
                model.u[r,s] >= model.u[i,j] + 1
                    - model.BigM * (1 - model.x[i,j,r,s]) + (model.BigM - 2) * model.x[r,s,i,j]
        )

    def __set_visitation_order_constraints(self) -> None:
        self._model.visitation_order_constraints = pyo.Constraint(
            self._model.K,
            rule= lambda model, k:
                model.u[model.N.at(k)] == 1 if k == 1 else
                model.u[model.N.at(k)] == model.BigM if k == len(model.N) else
                model.u[model.N.at(k)] >= model.u[model.N.at(k-1)]
                    + TaxicabDistance.calculate(model.N.at(k), model.N.at(k-1))
        )
