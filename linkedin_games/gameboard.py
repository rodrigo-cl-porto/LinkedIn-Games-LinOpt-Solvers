import networkx as nx
import pyomo.environ as pyo


class GameBoard:

    def __init__(self, board_dims:tuple[int, int]) -> None:
        self.board_dims = board_dims
        GameBoard._build_board(self)
        self._model: pyo.ConcreteModel | None = None
        self._stale: bool = True


    def __hash__(self):
        return hash(self._board_dims)
    
    
    def __len__(self):
        m, n = self._board_dims
        return m * n


    def __abs__(self):
        return len(self)


    @property
    def board_dims(self) -> tuple[int, int]:
        return self._board_dims

    @board_dims.setter
    def board_dims(self, value:tuple[int, int] = (2, 2)) -> None:
        
        if len(value) != 2:
            msg = f"Board dimensions must be a pair (m,n). Got {value!r} instead."
            raise TypeError(msg)
        
        if any(not isinstance(dim, int) or isinstance(dim, bool) for dim in value):
            msg = f"Board dimensions must be integers. Got {value!r} instead."
            raise TypeError(msg)
        
        if any(dim < 1 for dim in value):
            msg = f"Board dimensions must be positive. Got {value!r} instead."
            raise ValueError(msg)
        
        m, n = value
        if m * n < 2:
            msg = f"The board is too small for the game! Got a board dimension of {value!r}."
            raise ValueError(msg)

        if not isinstance(value, tuple):
            print((
                "WARNING: in order to avoid unexpected behaviours, board dimensions should be a tuple."
                f"Got a {type(value).__name__} instead."
            ))
            self._board_dims = tuple(value)
        else:
            self._board_dims = value
        
        self._stale = True


    @property
    def board(self) -> nx.Graph:
        return self._board
    
    def _build_board(self) -> None:
        board = nx.grid_2d_graph(*self._board_dims).to_directed()
        nx.set_node_attributes(board, name="value", values=None)
        nx.set_edge_attributes(board, name="value", values=None)
        self._board = board
        self._stale = True


    @property
    def board_squares(self) -> dict[tuple[int, int]: int]:
        return {(i+1, j+1): data["value"] for (i, j), data in self._board.nodes(data=True)}
    
    @property
    def board_edges(self):
        return {((i+1, j+1), (r+1, s+1)): data["value"] for ((i, j), (r, s)), data in self._board.edges(data=True)}
    

    @property
    def model(self) -> pyo.ConcreteModel:
        return self._model
