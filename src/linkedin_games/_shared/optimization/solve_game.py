from pprint import pprint

from pyomo.environ import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

from ..domain.game_grid import GameGrid
from ..domain.use_case import UseCase
from .modeler.factory import OptModelerFactory
from .solution._factory import GameSolutionFactory


class SolveGame(UseCase):

    def __init__(self, game: GameGrid) -> None:
        self._game = game
        self._opt_model = OptModelerFactory.create_modeler(game).build_model(game)

    def execute(self, solver: str="highs", verbose: bool=False) -> None:
        result = SolverFactory(solver).solve(self._opt_model)
        is_solved: bool = (
            result.Solver.status == SolverStatus.ok # Checks if solver is finished with normal termination and if...
            and (
                result.Solver.termination_condition == TerminationCondition.optimal # ended with an optimal solution...
                or result.Solver.termination_condition == TerminationCondition.feasible # or with a feasible one.
            )
        )
        if is_solved:
            print("Game solved successfully!")
            solution = GameSolutionFactory.create(self._game).build(self._opt_model)
            self._game.set_solution(solution)
            if verbose:
                print("SOLUTION:")
                pprint(self._game.solution)
            return
        msg = "No feasible solution was found!"
        if verbose:
            msg += f"\n\n{result.Solver}"
        raise RuntimeError(msg)
