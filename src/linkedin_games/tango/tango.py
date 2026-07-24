from pprint import pprint
from typing import Self

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..game_board import GameBoard


class Tango(GameBoard):

    def __init__(self,
            filled_squares:dict[tuple[int, int]: int] | None,
            matching_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None = None,
            opposite_pairs:set[tuple[tuple[int, int], tuple[int, int]]] | None = None,
            ) -> Self:
        # It's assumed that Tango board dimensions will always be a 6x6
        super().__init__(board_dims=(6,6))
        self.matching_pairs = matching_pairs
        self.opposite_pairs = opposite_pairs
        self.filled_squares = filled_squares


    def __hash__(self) -> int:
        return hash((
            self._dims,
            self._matching_pairs,
            self._opposite_pairs,
            self._filled_squares
        ))


    @property
    def matching_pairs(self) -> tuple[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        Return the pairs of squares that are separated by a equal (=) sign, 
        i.e. the squares that must have the same symbol.
        """
        return self._matching_pairs
    
    @matching_pairs.setter
    def matching_pairs(self, 
            values:tuple[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
        if values is None:
            self._matching_pairs = values
            return None

        invalid_items = [
            pair for pair in values if not isinstance(pair, tuple) or len(pair) != 2
        ]
        if invalid_items:
            msg = (
                "matching_pairs must be a collection of pairs of tuples."
                f" Got the following invalid pairs: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in values for square in pair
            if not isinstance(square, tuple)
        ]
        if invalid_items:
            msg = (
                "Squares in pair must be tuples of positive integers."
                f" Got the following invalid squares: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in values for square in pair for coord in square
            if not isinstance(coord, int) or coord < 1
        ]
        if invalid_items:
            msg = (
                "Coordinates must be positive integers."
                f" Got the following invalid squares: {invalid_items!r}."
            )
            raise ValueError(msg)

        invalid_items = [
            pair for pair in values if super()._manhattan_distance(*pair) != 1
        ]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones. "
                f"Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)
        
        if not isinstance(values, tuple):
            self._matching_pairs = tuple(values)
        else:
            self._matching_pairs = values
        
        self._stale = True


    @property
    def opposite_pairs(self) -> tuple[tuple[tuple[int, int], tuple[int, int]]] | None:
        """
        Return the pairs of squares that are separated by a cross (×) sign, i.e.
        the squares that must have opposite symbols.
        """
        return self._opposite_pairs
    
    @opposite_pairs.setter
    def opposite_pairs(self,
            value:tuple[tuple[tuple[int, int], tuple[int, int]]] | None) -> None:
        
        if value is None:
            self._opposite_pairs = value
            return None

        invalid_items = [
            pair for pair in value if not isinstance(pair, tuple) or len(pair) != 2
        ]
        if invalid_items:
            msg = (
                "opposite_pairs must be a collection of pairs of tuples."
                f" Got the following invalid pairs: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in value for square in pair
            if not isinstance(square, tuple)
        ]
        if invalid_items:
            msg = (
                "Squares in pair must be tuples of positive integers."
                f" Got the following invalid squares: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        invalid_items = [
            square for pair in value for square in pair for coord in square
            if not isinstance(coord, int) or coord < 1
        ]
        if invalid_items:
            msg = (
                "Coordinates must be positive integers."
                f" Got the following invalid squares: {invalid_items!r}."
            )
            raise ValueError(msg)

        invalid_items = [
            pair for pair in value if super()._manhattan_distance(*pair) != 1
        ]
        if invalid_items:
            msg = (
                "Squares in a pair must be consecutive ones."
                f" Got the following invalid pairs: {invalid_items!r}."
            )
            raise ValueError(msg)
        
        if not isinstance(value, tuple):
            self._opposite_pairs = tuple(value)
        else:
            self._opposite_pairs = value
        
        self._stale = True


    @property
    def filled_squares(self) -> dict[tuple[int, int]: int]:
        """Return the squares that are already filled with a symbol."""
        return self._filled_squares
    
    @filled_squares.setter
    def filled_squares(self, values:dict[tuple[int, int]: int]) -> None:

        if len(values) > len(self):
            msg = (
                "The number of filled squares exceeds the amount of board squares!"
                f" Got {len(values)} filled squares."
            )
            raise ValueError(msg)

        if not isinstance(values, dict):
            msg = (
                "filled_squares must be a dictionary."
                f" Got a {type(values).__name__} type instead."
            )
            raise ValueError(msg)

        invalid_items = {
            square: value
            for square, value in values.items()
            if value != 1 and value != 0
        }
        if invalid_items:
            msg = (
                "The square values must be of binary type. "
                f"Got the following invalid values: {invalid_items!r}."
            )
            raise TypeError(msg)
        
        self._filled_squares = {
            square: (1 if value else 0)
            for square, value in values.items()
        }


    def _construct_model(self) -> None:
        model = self.model

        # RANGE SETS
        I = model.I # Rows
        J = model.J # Columns

        # COMPOSITE SETS
        S = model.S # Board Squares
        K = model.K = pyo.Set(initialize=self.filled_squares.keys(), dimen=2)
        M = model.M = pyo.Set(initialize=self.matching_pairs)
        O = model.O = pyo.Set(initialize=self.opposite_pairs)

        # DECISION VARIABLES
        x = model.x = pyo.Var(S, within=pyo.Binary)

        # PARAMETERS
        m = model.m # Total number of rows
        n = model.n # Total number of columns
        k = model.k = pyo.Param( # Filled values
            K, initialize=self._filled_squares, within=pyo.Binary
        )

        # OBJECTIVE FUNCTION
        model.obj = pyo.Objective(expr=0) # feasibility problem

        # CONSTRAINTS
        model.equal_moons_suns_per_row_constraints = pyo.Constraint(
            I, rule=lambda model, i: sum(x[i, j] for j in J) == n / 2
        )
        model.equal_moons_suns_per_column_constraints = pyo.Constraint(
            J, rule=lambda model, j: sum(x[i,j] for i in I) == m / 2
        )
        model.no_three_consecutive_moons_per_row_constraints = pyo.Constraint(
            I, pyo.RangeSet(n-2),
            rule=lambda model, i, j: x[i, j] + x[i, j+1] + x[i, j+2] <= 2
        )
        model.no_three_consecutive_suns_per_row_constraints = pyo.Constraint(
            I, pyo.RangeSet(n-2),
            rule=lambda model, i, j: x[i, j] + x[i, j+1] + x[i, j+2] >= 1
        )
        model.no_three_consecutive_moons_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(m-2), J,
            rule=lambda model, i, j: x[i, j] + x[i+1, j] + x[i+2, j] <= 2
        )
        model.no_three_consecutive_suns_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(m-2), J,
            rule=lambda model, i, j: x[i, j] + x[i+1, j] + x[i+2, j] >= 1
        )
        model.matching_pairs_constraints = pyo.Constraint(
            M, rule=lambda model, i, j, r, s: x[i, j] - x[r, s] == 0
        )
        model.opposite_pairs_constraints = pyo.Constraint(
            O, rule=lambda model, i, j, r, s: x[i, j] + x[r, s] == 1
        )
        model.already_filled_squares_constraints = pyo.Constraint(
            K, rule=lambda model, i, j: x[i, j] == k[i, j]
        )


    def _set_solution(self, verbose:bool=False):
        nx.set_node_attributes(
            self._board,
            name="value",
            values={
                (i-1, j-1): round(pyo.value(self.model.x[i,j]))
                for i, j in self.model.S
            }
        )
        if verbose:
            print("Tango solution:")
            pprint(self.board_squares)


    def _show(self) -> None:
        plt.figure(figsize=(3.4, 3.4))
        pos = {(i, j): (j, -i) for i, j in self.board.nodes()}
        nx.draw(
            self.board,
            pos= pos,
            with_labels= True,
            labels= nx.get_node_attributes(self.board, "value"),
            node_size= 1000,
            node_color= [
                "#EEEAE7" if (i+1,j+1) in self.filled_squares else "white"
                for (i, j) in self.board.nodes()
            ],
            node_shape="s",
            edgecolors="#EEEAE7",
            linewidths= 1,
            width= 0,
            edgelist = [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.model.O] + [
                ((i-1, j-1), (r-1,s-1)) for i,j,r,s in self.model.M
            ]
        )
        nx.draw_networkx_edge_labels(
            self._board,
            pos= pos,
            edge_labels= {
                ((i-1, j-1), (r-1,s-1)): "×" for i,j,r,s in self.model.O} | {
                ((i-1, j-1), (r-1,s-1)): "=" for i,j,r,s in self.model.M
            },
            font_color="#887658"
        )
        plt.show()
