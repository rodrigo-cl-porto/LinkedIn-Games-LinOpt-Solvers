from pyomo.environ import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

from ..domain.game_grid import GameGrid
from ..domain.use_case import UseCase
from .models.factory import OptimizationModelBuilderFactory
from .solutions._factory import GameSolutionFactory


class SolveGame(UseCase):

    def __init__(self, game: GameGrid) -> None:
        self._game = game
        self._opt_model = OptimizationModelBuilderFactory.create(game).build()


    def execute(self, solver: str="highs", verbose: bool=False) -> GameGrid:
        result = SolverFactory(solver).solve(self._opt_model)
        is_solved: bool = (
            result.Solver.status == SolverStatus.ok # Checks if solver is finished with normal termination and if...
            and (
                result.Solver.termination_condition == TerminationCondition.optimal # ended with an optimal solution...
                or result.Solver.termination_condition == TerminationCondition.feasible # or with a feasible one.
            )
        )

        if is_solved:
            print(f"{type(self._game).__name__} game solved successfully!")
            solution = GameSolutionFactory.create(self._game).build(self._opt_model)
            self._game.set_solution(solution)
            return self._game

        msg = "No feasible solution was found!"
        if verbose:
            msg += f"\n\n{result.Solver}"
        
        raise RuntimeError(msg)
