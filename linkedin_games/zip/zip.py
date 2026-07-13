from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..gameboard import GameBoard


class Zip(GameBoard):

    def __init__(self, board_dims: tuple[int, int], numbered_squares: dict[tuple[int, int]: int], walls: tuple[tuple[int, int]] | None = None):
        super().__init__(board_dims)
        self.numbered_squares = numbered_squares
        self.walls = walls


    def __hash__(self):
        return hash((self._board_dims, self._numbered_squares, self._walls))


    @property
    def numbered_squares(self) -> dict[tuple[int, int]: int]:
        """Returns the dictionary of numbered squares on the game board, where the keys are (row, column) coordinates and the values are the corresponding numbers assigned to those squares."""
        return self._numbered_squares
    
    @numbered_squares.setter
    def numbered_squares(self, values:dict[tuple[int, int]: int]) -> None:

        if len(values) > len(self):
            msg = (
                "The number of numbered squares exceeds the amount of board squares! "
                f"Got {len(values)} numbered squares, while the game board has {len(self)} squares."
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

        elif not isinstance(values, dict):
            msg = "The numbered squares must be a dictionary."
            raise ValueError(msg)
        
        else:
            self._numbered_squares = values

        nx.set_node_attributes(self.board, name="value", values=None)
        nx.set_node_attributes(self.board, name="value", values=self.numbered_squares)
        self._stale = True


    @property
    def walls(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Returns a tuple of walls (pairs of squares)"""
        return self._walls
    
    @walls.setter
    def walls(self, values:tuple[tuple[int, int], tuple[int, int]]) -> None:

        if len(values) > len(self.board.edges) / 2:
            msg = (
                "The number of walls exceeds the amount of board edges! "
                f"Got {len(values)} numbered squares, while the game board has {len(self.board.edges) / 2} squares."
            )
            raise ValueError(msg)

        if isinstance(values, list):
            print((
                "WARNING: The walls should be a tuple of squares. "
                f"Got a {type(values).__name__} instead."
            ))
            self._walls = tuple(values)

        elif not isinstance(values, tuple):
            msg = "Walls must be a tuple of squares."
            raise ValueError(msg)
        
        else:
            self._walls = values

        invalid_items = [pair for pair in values if GameBoard.__manhathan_distance(*pair) != 1]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)

        self._stale = True


    @property
    def path(self) -> list[tuple[int, int]]:
        """Returns the path that solves the game, as a list of (row, column) coordinates."""
        return [(i+1, j+1) for (i, j) in self._path]


    def _construct_model(self) -> None:

        model = self.model

        # RANGE SETS
        I = model.I # Rows
        J = model.J # Columns

        # COMPOSITE SETS
        S = model.S # Board Squares
        E = model.E = pyo.Set(initialize=lambda model: [
            ((i, j), (i+1, j)) for i in I for j in J if i+1 in I] + [
            ((i, j), (i-1, j)) for i in I for j in J if i-1 in I] + [
            ((i, j), (i, j+1)) for i in I for j in J if j+1 in J] + [
            ((i, j), (i, j-1)) for i in I for j in J if j-1 in J]
        ) # Edges
        K = model.K = pyo.Set(initialize=self.numbered_squares.keys(), dimen=2)
        W = model.W = pyo.Set(initialize=self.walls) # Walls
        
        # DECISION VARIABLES
        x = model.x = pyo.Var(E, within=pyo.Binary, initialize=0)
        u = model.u = pyo.Var(S, within=pyo.NonNegativeReals)

        # PARAMETERS
        k = model.k = pyo.Param(S, initialize=self.numbered_squares, default=0, within=pyo.NonNegativeIntegers)

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0) # feasibility problem
    
        # CONSTRAINTS
        model.outgoing_edges_constraints = pyo.Constraint(
            S,
            rule=lambda model, i, j: \
                sum(x[(i,j),w] for w in S if ((i,j),w) in E) == 1 if k[i,j] != len(K) else \
                sum(x[(i,j),w] for w in S if ((i,j),w) in E) == 0
        )
        
        model.incoming_edges_constraints = pyo.Constraint(
            S,
            rule=lambda model, i, j: \
                sum(x[s,(i,j)] for s in S if (s,(i,j)) in E) == 1 if k[i,j] != 1 else \
                sum(x[s,(i,j)] for s in S if (s,(i,j)) in E) == 0
        )
    
        if W is not None:
            model.wall_constraints = pyo.Constraint(
                W,
                rule=lambda model, i, j, r, s: x[i,j,r,s] + x[r,s,i,j] == 0
            )

        M = len(self)
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


    def _set_solution(self, verbose:bool=False) -> None:

        nx.set_node_attributes(
            self.board,
            name="value",
            values={
                (i-1, j-1): round(pyo.value(self.model.u[i,j]))
                for i, j in self.model.S
            }
        )

        nx.set_edge_attributes(
            self.board,
            name="value",
            values={
                ((i-1, j-1), (r-1, s-1)): round(pyo.value(self.model.x[i,j,r,s]))
                for i, j, r, s in self.model.E
            }
        )

        path = nx.get_node_attributes(self.board, "value")
        self._path = sorted(path.keys(), key=path.get)

        if verbose:
            print("This is the path that solves the games:")
            pprint(self.path)


    def _show(self) -> None:

        plt.figure(figsize=(3.4, 3.4))

        path_color:str="#EE5F12"
        
        nx.draw(
            self.board,
            pos= {(i,j): (j,-i) for i, j in self.board.nodes()},
            with_labels= True,
            labels= {(i-1, j-1): self.model.k[i,j] for (i, j) in self.model.K},
            arrows=False,
            node_shape="o", # round nodes
            node_size= 1000,
            node_color= [
                "white" if (i+1,j+1) in self.numbered_squares else path_color
                for (i,j) in self.board.nodes()
            ],
            edge_color= path_color,
            edgecolors= path_color,
            linewidths= 3,
            width= 35,
            edgelist= [
                ((i-1, j-1), (r-1, s-1)) 
                for i,j,r,s in self.model.E
                if int(pyo.value(self.model.x[i,j,r,s])) == 1
            ]
        )

        plt.show()
