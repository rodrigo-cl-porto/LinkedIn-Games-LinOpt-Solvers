from pyomo.environ import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

from ..domain.games.game_grid import GameGrid
from ..domain.use_case import UseCase
from .models._director import OptimizationModelDirector
from .solutions._factory import GameSolutionBuilderFactory


class SolveGame(UseCase):

    def __init__(self, game: GameGrid) -> None:
        self._game = game
        self._opt_model = OptimizationModelDirector.build_opt_model(game)
        self._is_solved = False


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
            self._game.solution = GameSolutionBuilderFactory.create_builder(self._game).build(self._opt_model)
            return self._game

        msg = "No feasible solution was found!"
        if verbose:
            msg += f"\n\n{result.Solver}"
        
        raise RuntimeError(msg)
