"""
The module includes basic structures that represents a status of a blokus session.
"""

from enum import Enum

from game.blokus_exception import InvalidPlacementError
import game.distance as distance

class BlokusSquareData(Enum):
    """Class which represents a data in a square of the blokus board."""
    EMPTY = 0
    RED_3 = 3
    RED_4 = 4
    RED_5 = 5
    BLUE_3 = -3
    BLUE_4 = -4
    BLUE_5 = -5

    def is_red(self):
        """Returns True if the data represents Red cell"""
        return self is BlokusSquareData.RED_3 or \
            self is BlokusSquareData.RED_4 or \
            self is BlokusSquareData.RED_5

    def is_blue(self):
        """Returns True if the data represents Blue cell"""
        return self is BlokusSquareData.BLUE_3 or \
            self is BlokusSquareData.BLUE_4 or \
            self is BlokusSquareData.BLUE_5

    @staticmethod
    def get_data(placement, is_red):
        """Obtain the data corresponding to the placement"""
        target_num = len(placement)
        if not is_red:
            target_num *= -1

        return BlokusSquareData(target_num)


class BlokusBoard:
    """Class which represents a board of blokus game"""

    def __init__(self, size=12):
        """
        The size of the board is defined as a number of squares on a side.
        Hence the board will have 'size ** 2' number of squares.
        """
        self._size = size
        self._board = [[BlokusSquareData.EMPTY] * size] * size

    def get_placement_at(self, coordinate):
        """
        Obtain the placement at the specified coordinate on the board.

        Placement information will be returned as BlokusSquareData.
        ValueError is raised when the coordinate is out of range.
        """
        x_coord, y_coord = coordinate
        if x_coord >= self._size or y_coord >= self._size:
            raise ValueError("x or y is out of range! x: {0}, y: {1}".format(x_coord, y_coord))
        return self._board[x_coord][y_coord]

    def get_size(self):
        """Obtain the size of the board."""
        return self._size

    def set(self, cell, data):
        """Set the data to the specified cell"""
        self._board[cell[0]][cell[1]] = data

class BlokusGame:
    """Class which represents a game session."""

    def __init__(self, board_size=12):
        self._board = BlokusBoard(size=board_size)
        self.has_red_played = False
        self.has_blue_played = False

        self.is_red_next = True


    def _is_placement_continuous(self, placement):
        placement_num = len(placement)

        for i in range(placement_num):
            check_target_cell = placement[i]
            is_adjuscent_found = False

            for j in range(placement_num):
                if j == i:
                    continue

                if distance.manhattan_2d(check_target_cell, placement[j]) == 1:
                    is_adjuscent_found = True
                    break

            if not is_adjuscent_found:
                return False
        return True

    def _is_placement_target_empty(self, placement_list):
        for placement in placement_list:
            old_placement = self._board.get_placement_at(placement)
            if old_placement is not BlokusSquareData.EMPTY:
                return False
        return True

    def _is_first_cell_covered(self, placement_list):
        """Returns true if and only if the placement is the first action and
        the beginning cell is covered."""
        if self.is_red_next:
            return self.has_red_played and ([2, 2] in placement_list)
        else:
            return self.has_blue_played and ([9, 9] in placement_list)

    def _is_placement_compatible(self, placement_list):
        corner_vectors = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        adjacent_vectors = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        is_on_corner = False
        for cell in placement_list:
            if not is_on_corner:
                # check if the cell is on a corner of existing player region
                for vector in corner_vectors:
                    target_coord = [cell[0] + vector[0], cell[1] + vector[1]]
                    target_cell = self._board.get_placement_at(target_coord)

                    if self.is_red_next:
                        is_on_corner = target_cell.is_red()
                    else:
                        is_on_corner = target_cell.is_blue()

                    if is_on_corner:
                        break

            # check that the cell is not on a side of existing player region
            for vector in adjacent_vectors:
                target_coord = [cell[0] + vector[0], cell[1] + vector[1]]
                target_cell = self._board.get_placement_at(target_coord)

                if self.is_red_next and target_cell.is_red():
                    return False
                elif not self.is_red_next and target_cell.is_blue():
                    return False

        return is_on_corner

    def _is_placement_valid(self, placement):
        placement_num = len(placement)
        if placement_num < 3 or placement_num > 5:
            return False

        return (self._is_placement_continuous(placement) and
                self._is_placement_target_empty(placement) and
                (self._is_first_cell_covered(placement) or
                 self._is_placement_compatible(placement)))

    def place(self, blokus_placement_list):
        """
        Execute a given placement.
        Returns True when executed successfully.

        Raises InvalidPlacementError when the placement is invalid.
        """
        if not self._is_placement_valid(blokus_placement_list):
            raise InvalidPlacementError(self, blokus_placement_list)

        placement_data = BlokusSquareData.get_data(blokus_placement_list, self.is_red_next)
        for coord in blokus_placement_list:
            self._board.set(coord, placement_data)

        if self.is_red_next:
            self.has_red_played = True
        else:
            self.has_blue_played = True

        self.is_red_next = not self.is_red_next
        return True
