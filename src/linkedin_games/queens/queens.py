from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..game_board import GameBoard
from .region import Region


class Queens(GameBoard):
    """A Queens is board game with colored regions"""

    def __init__(self, board_dims:tuple[int, int], regions:set[Region]) -> None:
        super().__init__(board_dims)
        self.regions = regions


    def __hash__(self):
        return hash((self._board_dims, self._regions))


    @property
    def regions(self) -> set[Region]:
        """Returns the set of Region objects representing the colored regions on the board. It's assumed that the regions are non-overlapping and cover the entire board."""
        return self._regions

    @regions.setter
    def regions(self, values:set[Region]) -> None:

        if not isinstance(values, set):
            msg = "Regions must be a set of Region classes."
            raise TypeError(msg)
        
        if len(values) < 1:
            msg = "The set of Regions cannot be empty!"
            raise ValueError(msg)
        
        if any(not isinstance(region, Region) for region in values):
            msg = "All elements of the set must be Region classes."
            raise TypeError(msg)
        
        if len(values) != len({region.color for region in values}):
            msg = "There must not be two regions with the same color."
            raise ValueError(msg)
        
        all_region_squares = [square for region in values for square in region.squares]
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
        
        nx.set_node_attributes( # Adding a color for each square on the board
            self._board,
            name="color",
            values={(i-1, j-1): region.color for region in values for (i, j) in region.squares}
        )

        self._regions = values
        self._stale = True


    @property
    def crowns(self) -> tuple[tuple[int, int]]:
        """The solution of the game, i.e. the squares that contain a crown."""
        return sorted(tuple((i+1, j+1) for (i,j) in self.__crowns.nodes()))


    def _construct_model(self):

        model = self.model

        # RANGE SETS
        I = model.I # Rows
        J = model.J # Columns
        K = model.K = pyo.Set(initialize=[region.color for region in self.regions]) # Regions

        # COMPOSITE SETS
        S = model.S # Board Squares
        R = model.R = pyo.Set(K, initialize={region.color: region.squares for region in self.regions}, dimen=2) # Region Squares
        D = model.D = pyo.Set(initialize=lambda model: [ # Diagonals
            ((i, j), (i+1, j+1)) for (i, j) in S if (i+1, j+1) in S] + [
            ((i, j), (i+1, j-1)) for (i, j) in S if (i+1, j-1) in S
        ])

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


    def _set_solution(self, verbose:bool=False) -> None:

        nx.set_node_attributes(
            self.board,
            name="value",
            values= {(i-1, j-1): int(pyo.value(self.model.x[i,j])) for (i, j) in self.model.S}
        )

        crowns = [square for square, value in nx.get_node_attributes(self.board, "value").items() if value == 1]
        self.__crowns = self.board.subgraph(crowns)

        if verbose:
            print("These are the squares that contain a crown:")
            pprint(self.crowns)


    def _show(self) -> None:

        plt.figure(figsize=(3.4, 3.4))

        nx.draw(
            self.board,
            pos= {(i, j): (j, -i) for i, j in self.board.nodes()},
            with_labels= True,
            labels= {square: "O" for square in self.__crowns.nodes()},
            node_size= 1000,
            node_color= [color for color in nx.get_node_attributes(self.board, "color").values()],
            node_shape="s", # Squared-shape nodes
            width=0
        )
        
        plt.show()
