from ..domain.game_grid import GameGrid
from ..domain.use_case import UseCase
from .renderers._factory import GameRendererFactory


class ShowGame(UseCase):

    def __init__(self, game: GameGrid) -> None:
        self._game = game
        self._renderer = GameRendererFactory.create_renderer(game)


    def execute(self) -> None:
        self._renderer.show()
