from typing import Self

import pyomo.environ as pyo

from ...domain.games.zip.zip import Zip
from ...domain.utils.taxicab_distance import TaxicabDistance
from ._builder import OptimizationModelBuilder


class ZipModelBuilder(OptimizationModelBuilder[Zip]):
    
    def set_range_sets(self) -> Self:
        super().set_range_sets()
        self._model.K = pyo.RangeSet(len(self._game.numbered_squares))
        return self


    def set_composite_sets(self) -> Self:
        super().set_composite_sets()
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
        return self


    def set_parameters(self) -> Self:
        self._model.BigM = self._model.m * self._model.n
        return self


    def set_decision_variables(self) -> Self:
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
        return self


    def set_objective_function(self) -> Self:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem
        return self


    def set_constraints(self) -> Self:
        return (
            self
            .set_edge_constraints()
            .set_blocked_path_contraints()
            .set_subroute_elimination_constraints()
            .set_visitation_order_constraints()
        )


    def set_edge_constraints(self) -> Self:
        neighbors = { # This dictionary is important to access all neighbors of a square quickly.
            (i, j): [
                (r, c) for r, c in [
                    (i-1, j),
                    (i+1, j),
                    (i, j-1),
                    (i, j+1)
                ] if (r, c) in self._model.S
            ] for (i, j) in self._model.S
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
        return self


    def set_blocked_path_contraints(self) -> Self:
        self._model.wall_constraints = pyo.Constraint(
            self._model.W,
            rule=lambda model, i, j, r, s: model.x[i,j,r,s] + model.x[r,s,i,j] == 0
        )
        return self


    def set_subroute_elimination_constraints(self) -> Self:
        self._model.miller_tucker_zemlin_constraints = pyo.Constraint(
            self._model.E,
            rule=lambda model, i, j, r, s:
                model.u[r,s] >= model.u[i,j] + 1
                    - model.BigM * (1 - model.x[i,j,r,s]) + (model.BigM - 2) * model.x[r,s,i,j]
        )
        return self


    def set_visitation_order_constraints(self) -> Self:
        self._model.visitation_order_constraints = pyo.Constraint(
            self._model.K,
            rule= lambda model, k:
                model.u[model.N.at(k)] == 1 if k == 1 else
                model.u[model.N.at(k)] == model.BigM if k == len(model.N) else
                model.u[model.N.at(k)] >= model.u[model.N.at(k-1)]
                    + TaxicabDistance.calculate(model.N.at(k), model.N.at(k-1))
        )
        return self
