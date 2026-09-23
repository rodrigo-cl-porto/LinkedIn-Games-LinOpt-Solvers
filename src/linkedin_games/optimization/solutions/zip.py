from pyomo.environ import ConcreteModel

from ._game_solution import GameSolution


class ZipSolution(GameSolution):

    def __init__(self, model: ConcreteModel) -> None:
        ...


    def _set_solution(self, verbose:bool=False) -> None:

        S = self.model.S
        E = self.model.E
        u = self.model.u
        x = self.model.x

        nx.set_node_attributes(
            self.grid,
            name="value",
            values={(i-1, j-1): round(pyo.value(u[i,j])) for i, j in S}
        )
        nx.set_edge_attributes(
            self.grid,
            name="value",
            values={((i-1, j-1), (r-1, s-1)): round(pyo.value(x[i,j,r,s])) for i, j, r, s in E}
        )
        path = nx.get_node_attributes(self.grid, "value")
        path = sorted(path.keys(), key=path.get)
        self.__path = [(i+1, j+1) for (i, j) in path]
        if verbose:
            print("This is the path that solves the games:")
            pprint(self.path)