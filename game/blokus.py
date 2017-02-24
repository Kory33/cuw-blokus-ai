from enum import Enum


class BlokusSquareData(Enum):
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    PLAYER_3 = 3
    ENEMY_1 = -1
    ENEMY_2 = -2
    ENEMY_3 = -3


class BlokusBoard:
    """Class which represents a board of blokus game

    The size of the board is defined as a number of squares on a side.
    Hence the board will have 'size ** 2' number of squares."""

    def __init__(self, size=12):
        self._size = size
        self._board = [[BlokusSquareData.EMPTY] * size] * size

    """Obtain the placement at the specified coordinate on the board.

    Placement information will be returned as BlokusSquareData.
    ValueError is raised when the coordinate is out of range."""

    def get_placement_at(self, x, y):
        if x >= self.size or y >= self.size:
            raise ValueError("x or y is out of range! x: {0}, y: {1}".format(x, y))
        return self._board[x][y]

    """Obtain the size of the board."""

    def get_size(self):
        return self._size


class BlokusGame:
    """Class which represents a game session."""

    def __init__():
        pass
