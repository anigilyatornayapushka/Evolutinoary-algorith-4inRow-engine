from typing import (
    List,
    Optional,
)
from enum import Enum
from copy import deepcopy

from .exceptions import (
    OutOfRangeError,
    NoLastMoveError,
)


class GameState(Enum):
    """Different states of the game."""
    RUNNING = 0
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    DRAW = 3


class Side(Enum):
    """Different Player Sides."""
    A = 1
    B = 2


class Board:
    """Default board 6 x 7."""
    _rows: int
    _columns: int
    _mv_order: Side
    _board: List[List[Side]]
    _lst_mv: Optional[int] = None

    def __init__(self, mv_order: Side,
                 rows: int = 6, columns: int = 7) -> None:
        self._rows = rows
        self._columns = columns
        self._mv_order = mv_order
        self._board = [[] for _ in range(columns)]


    def _swtch_mv_order(self) -> None:
        self._mv_order = Side.A if self._mv_order == Side.B else Side.B


    def _validate_move(self, column: int) -> None:
        """Raises `OutOfRangeError()` if invalid move."""
        if not 0 <= column < self._columns or len(self._board[column]) == self._rows:
            raise OutOfRangeError()


    @property
    def board(self) -> List[List[Side]]:
        return deepcopy(self._board)


    def do_move(self, column: int) -> None:
        """
        Simply add a piece on the board depending of whos turn to move.

        Throws:
            - OutOfRangeError()
        """
        try:
            self._validate_move(column)
        except OutOfRangeError as err:
            raise err

        self._lst_mv = column
        self._board[column].append(self._mv_order)
        self._swtch_mv_order()


    def cancel_move(self) -> None:
        """
        Cancles last move in the board.

        Throws:
            - NoLastMoveError()
        """
        if self._lst_mv is None:
            raise NoLastMoveError()

        self._board[self._lst_mv].pop()
        self._swtch_mv_order()
        self._lst_mv = None


    def get_state_by_last_move(self) -> GameState:
        """
        Returns state of the game calculating position around last move.

        Throws:
            - NoLastMoveError()
        """
        state_checker = StateChecker(
            self._rows, self._columns, self.board)
        try:
            game_state = state_checker.get_state_by_last_move(
                self._mv_order, self._lst_mv)
        except NoLastMoveError as err:
            raise err

        return game_state


class StateChecker:
    """Check current state of `Board` depending of last move."""
    _rows: int
    _cols: int
    _height: int
    _width: int
    _mv_order: Side
    _board: List[List[Side]]

    def __init__(self, rows: int, columns: int,
                 board: List[List[Side]],
                 lst_mv: Optional[int],
                 mv_order: Side) -> None:
        """
        Throws:
            - NoLastMoveError()
        """
        self._rows = rows
        self._cols = columns
        self._board = board
        self._mv_order = mv_order

        if lst_mv is None:
            raise NoLastMoveError()

        self._height: int = self._h(lst_mv)
        self._width: int = lst_mv


    def __counter(self, rng: range, *, dx: int = 1, dy: int = 0) -> int:
        """
        rng = range(start, end, step) -
        param for iteration in neighbourhood

        dx, dy are responsible for direction of shifting
        They are either 1 or -1 or 0 if not use.
        """
        counter = 0
        for delta in rng:
            col: int = self._width + delta * dx
            row: int = self._height + delta * dy
            if (col < 0 or row < 0 or col >= self._cols
                    or row >= self._rows or self._h(col) < row
                    or self._board[col][row]
                    != self._board[self._width][self._height]):
                break
            counter += 1
        return counter


    def __define_winner(self, counter: int) -> Optional[GameState]:
        """Define who won (if any) by move order."""
        if counter >= 4:
            if self._mv_order == Side.A:
                # Since side was switched after a move
                return GameState.PLAYER_2_WIN
            return GameState.PLAYER_1_WIN
        return None


    def _h(self, column: int) -> int:
        """Return index of the last element
        in the column or -1 for empty."""
        return len(self._board[column]) - 1


    def _vert_check(self) -> Optional[GameState]:
        counter = (1 + self.__counter(range(1,4), dx=0, dy=-1))
        return self.__define_winner(counter)


    def _horiz_check(self) -> Optional[GameState]:
        counter = (1 + self.__counter(range(-1, -4, -1))
                   + self.__counter(range(1,4)))
        return self.__define_winner(counter)


    def _diag_check(self) -> Optional[GameState]:
        counter1 = (1 + self.__counter(range(-1, -4, -1), dx=1, dy=1)
                    + self.__counter(range(1,4), dx=1, dy=1))
        counter2 = (1 + self.__counter(range(-1, -4, -1), dx=1, dy=-1)
                    + self.__counter(range(1,4), dx=1, dy=-1))
        if res := self.__define_winner(counter1):
            return res
        return self.__define_winner(counter2)


    def get_state_by_last_move(self) -> GameState:
        """
        Returns state of the game
        calculating position around last move.
        """
        check1: Optional[GameState] = self._vert_check()
        check2: Optional[GameState] = self._horiz_check()
        check3: Optional[GameState] = self._diag_check()
        check4: Optional[GameState] = None
        if all(len(col) == self._rows for col in self._board):
            check4 = GameState.DRAW

        return check1 or check2 or check3 or check4 or GameState.RUNNING
