from typing import (
    List,
    Optional,
)
from enum import Enum
from copy import deepcopy

from .exceptions import (
    FullColumnException,
    LastMoveDoesNotExistsException,
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
        self.board = [[] for _ in range(columns)]


    def _swtch_mv_order(self) -> None:
        self._mv_order = Side.A if self._mv_order == Side.B else Side.B


    def _validate_move(self, column: int) -> None:
        """Raises `LastMoveDoesNotExistsException()` if invalid move."""
        if (column < 0
                or column >= self._columns
                or self._board[column].__len__ == self._rows):
            raise LastMoveDoesNotExistsException()


    def _h(self, column: int) -> int:
        """Return index of the last element in the column."""
        return self._board.get(column).__len__ - 1


    def do_move(self, column: int) -> int:
        """
        Simply add a piece on the board depending of whos turn to move.

        Throws:
            - LastMoveDoesNotExistsException()
        """
        try:
            self._validate_move(column)
        except LastMoveDoesNotExistsException as err:
            raise err

        self._lst_mv = column
        self._board[column].append(self._mv_order)
        self._swtch_mv_order()


    def cancel_move(self) -> None:
        """
        Cancles last move in the board.

        Throws:
            - FullColumnException()
        """
        if not self._lst_mv:
            raise FullColumnException()

        self._board[self._lst_mv].pop()
        self._swtch_mv_order()


    def get_state_by_last_move(self) -> GameState:
        """
        Returns state of the game calculating position around last move.

        Throws:
            - FullColumnException()
        """
        if not self._lst_mv:
            raise FullColumnException()

        height: int = self._h(self._lst_mv)
        width: int = self._lst_mv

        # VERTICAL CHECK
        if (height >= 3 and  # Not less than 4 pieces in the column
                self._board[-1] == self._board[-2] ==
                self._board[-3] == self._board[-4]):
            if self._mv_order == Side.A:
                # Since side was switched after a move
                return GameState.PLAYER_2_WIN
            return GameState.PLAYER_1_WIN

        # HORIZONTAL CHECK
        counter = 1  # Counts same pieces in neighbourhood

        for delta in range(-1, -4, -1):  # Checking left side from -1 to -3
            col: int = width + delta
            if (col < 0 or self._h(col) < height or
                    self._board[col][height]
                    != self._board[width][height]):
                break
            counter += 1

        for delta in range(1, 4):  # Checking right side from +1 to +3
            col: int = width + delta
            if (col >= self._columns or self._h(col) < height or
                    self._board[col][height]
                    != self._board[width][height]):
                break
            counter += 1

        if counter >= 4:
            if self._mv_order == Side.A:
                # Since side was switched after a move
                return GameState.PLAYER_2_WIN
            return GameState.PLAYER_1_WIN

        # DIAGONAL CHECK
        counter = 1
        # Checking / diagonal
        for delta in range(-1, -4, -1):  # Checking left side from -1 to -3
            row: int = height + delta
            col: int = width + delta
            if (col < 0 or row < 0 or self._h(col) < row or
                    self._board[col][row]
                    != self._board[width][height]):
                break
            counter += 1

        for delta in range(1, 3):  # Checking right side from +1 to +3
            row: int = height + delta
            col: int = width + delta
            if (col >= self._columns or row >= self._rows
                    or self._h(col) < row or
                    self._board[col][row]
                    != self._board[width][height]):
                break
            counter += 1

        if counter >= 4:
            if self._mv_order == Side.A:
                # Since side was switched after a move
                return GameState.PLAYER_2_WIN
            return GameState.PLAYER_1_WIN

        counter = 1
        # Checking \ diagonal
        for delta in range(-1, -4, -1):  # Checking left side from -1 to -3
            row: int = height - delta
            col: int = width + delta
            if (col < 0 or row < 0 or self._h(col) < row or
                    self._board[col][row]
                    != self._board[width][height]):
                break
            counter += 1

        for delta in range(1, 3):  # Checking right side from +1 to +3
            row: int = height - delta
            col: int = width + delta
            if (col >= self._columns or row >= self._rows
                    or self._h(col) < row or
                    self._board[col][row]
                    != self._board[width][height]):
                break
            counter += 1

        if counter >= 4:
            if self._mv_order == Side.A:
                # Since side was switched after a move
                return GameState.PLAYER_2_WIN
            return GameState.PLAYER_1_WIN

        return GameState.RUNNING

    @property
    def board(self) -> List[List[int]]:
        return deepcopy(self._board)
