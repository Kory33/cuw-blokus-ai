"""
The module includes basic structures that represents a status of a blokus session.
"""

from enum import Enum

from game.blokus_exception import InvalidPlacementError
import game.distance as distance

class BlokusSquareData(Enum):
    """Class which represents a data in a square of the blokus board."""
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    PLAYER_3 = 3
    ENEMY_1 = -1
    ENEMY_2 = -2
    ENEMY_3 = -3


class BlokusBoard:
    """Class which represents a board of blokus game"""

    def __init__(self, size=12):
        """
        The size of the board is defined as a number of squares on a side.
        Hence the board will have 'size ** 2' number of squares.
        """
        self._size = size
        self._board = [[BlokusSquareData.EMPTY] * size] * size

    def get_placement_at(self, x_coord, y_coord):
        """
        Obtain the placement at the specified coordinate on the board.

        Placement information will be returned as BlokusSquareData.
        ValueError is raised when the coordinate is out of range.
        """
        if x_coord >= self._size or y_coord >= self._size:
            raise ValueError("x or y is out of range! x: {0}, y: {1}".format(x_coord, y_coord))
        return self._board[x_coord][y_coord]

    def get_size(self):
        """Obtain the size of the board."""
        return self._size


class BlokusPlacement:
    """
    Class which represents a placement.
    A placement is created once in each player turn, hence is a step in the game.
    """

    def __init__(self, placement_array, board_state):
        """
        placement_array is a two-dimentional array which stores pairs of coordinates.
        board_state is a status of the game board before the placement takes place.

        Raises an InvalidPlacementError when an illegal placement is given to the constructor.
        """
        self._placement = sorted(placement_array, lambda coord: coord[0])
        self._old_board_state = board_state

        if not self._is_placement_valid():
            raise InvalidPlacementError(board_state, placement_array)

    def _is_placement_valid(self):
        placement_num = len(self._placement)
        if placement_num < 3 or placement_num > 5:
            return False

        return self._is_placement_continuous()

    def _is_placement_continuous(self):
        placement_num = len(self._placement)

        for i in range(placement_num):
            check_target_cell = self._placement[i]
            is_adjuscent_found = False

            for j in range(placement_num):
                if j == i:
                    continue

                if distance.manhattan_2d(check_target_cell, self._placement[j]) == 1:
                    is_adjuscent_found = True
                    break

            if not is_adjuscent_found:
                return False
        return True

class BlokusGame:
    """Class which represents a game session."""

    def __init__(self, board_size=12):
        self._board = BlokusBoard(size=board_size)
