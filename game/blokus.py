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
        return self.value > 0

    def is_blue(self):
        """Returns True if the data represents Blue cell"""
        return self.value < 0

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
        self._board = []
        for i in range(size):
            self._board.append([BlokusSquareData.EMPTY] * size)

    def get_data_at(self, coordinate):
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
        self._has_red_played = False
        self._has_blue_played = False

        self.is_red_next = True

        self.red_remaining = [10, 5, 2]
        self.blue_remaining = [10, 5, 2]

    def _is_placement_continuous(self, cells):
        for check_target_cell in cells:
            is_adjacent_found = False

            for adjacent_candidate in cells:
                if check_target_cell == adjacent_candidate:
                    continue

                if distance.manhattan_2d(check_target_cell, adjacent_candidate) == 1:
                    is_adjacent_found = True
                    break

            if not is_adjacent_found:
                return False
        return True

    def _is_placement_target_empty(self, cells):
        for cell in cells:
            cell_data = self._board.get_data_at(cell)
            if cell_data.value is not 0:
                return False
        return True

    def _is_first_cell_covered(self, cells):
        """Returns true if and only if the placement is the first action and
        the beginning cell is covered."""
        if self.is_red_next:
            return not self._has_red_played and ((2, 2) in cells)
        else:
            return not self._has_blue_played and ((9, 9) in cells)

    def _is_same_color_found_on(self, cells, direction_vectors):
        """
        Returns true if there is at least one same-coloured cell from the new placement region
        towards the direction_vectors.

        direction_vectors should be a 2 dimentional array, each element representing a
        relative vector from the inspect target to the check direction.
        """
        for cell in cells:
            for vector in direction_vectors:
                target_coord = (cell[0] + vector[0], cell[1] + vector[1])
                if target_coord[0] < 0 or target_coord[0] >= self._board.get_size():
                    continue

                if target_coord[1] < 0 or target_coord[1] >= self._board.get_size():
                    continue

                target_cell_data = self._board.get_data_at(target_coord)

                if self.is_red_next and target_cell_data.is_red():
                    return True
                elif not self.is_red_next and target_cell_data.is_blue():
                    return True

        return False

    def _is_source_in_hand(self, cells):
        checktarget = []
        if self.is_red_next:
            checktarget = self.red_remaining
        else:
            checktarget = self.blue_remaining
        return checktarget[len(cells) - 3] > 0

    def _is_same_color_on_corner(self, cells):
        return self._is_same_color_found_on(cells, {(1, 1), (-1, 1), (-1, -1), (1, -1)})

    def _is_same_color_on_side(self, cells):
        return self._is_same_color_found_on(cells, {(1, 0), (0, 1), (-1, 0), (0, -1)})

    def _is_placement_valid(self, cells):
        cells_num = len(cells)
        if cells_num < 3 or cells_num > 5:
            return False

        return (self._is_placement_continuous(cells) and
                self._is_placement_target_empty(cells) and
                (self._is_first_cell_covered(cells) or
                 self._is_same_color_on_corner(cells)) and
                not self._is_same_color_on_side(cells) and
                self._is_source_in_hand(cells))

    def _is_available(self, cell):
        """
        Returns True when the player can place on the specified cell.
        This method only does empty check and adjacent-not-same-color check.
        """
        if not 0 <= cell[0] < self._board.get_size() or not 0 <= cell[1] < self._board.get_size():
            return False

        return (self._is_placement_target_empty({cell}) and
                not self._is_same_color_on_side({cell}))

    def place(self, cells_set):
        """
        Execute a given placement.
        Returns True when placed successfully.

        Raises InvalidPlacementError when the placement is invalid.
        """
        if not self._is_placement_valid(cells_set):
            raise InvalidPlacementError(self, cells_set)

        placement_data = BlokusSquareData.get_data(cells_set, self.is_red_next)
        for coord in cells_set:
            self._board.set(coord, placement_data)

        placement_num = len(cells_set)
        if self.is_red_next:
            self.red_remaining[placement_num - 3] -= 1
            self._has_red_played = True
        else:
            self.blue_remaining[placement_num - 3] -= 1
            self._has_blue_played = True

        self.is_red_next = not self.is_red_next
        return True

    def _get_initiatable_cells(self):
        initiatable_cells = set()

        if not self._has_red_played and self.is_red_next:
            return {(2, 2)}

        if not self._has_blue_played and not self.is_red_next:
            return {(9, 9)}

        # Obtain all the cells from which the placement can be started
        for column in range(self._board.get_size()):
            for row in range(self._board.get_size()):
                cell = (column, row)
                if self._is_available(cell) and self._is_same_color_on_corner(cell):
                    initiatable_cells.add(cell)

        return initiatable_cells

    def _search(self, placement_chain, remaining_search_size):
        """
        Returns all the placement pattern which can be created
        by adding `remaining_search_size` number of cells around the given placement chain.
        """
        search_direction = {(1, 0), (0, 1), (-1, 0), (0, -1)}

        search_result = set()

        # if the search should be terminated
        if remaining_search_size is 0:
            return {frozenset(placement_chain)}

        for cell in placement_chain:
            for direction in search_direction:
                new_cell = (cell[0] + direction[0], cell[1] + direction[1])
                if new_cell in placement_chain or not self._is_available(new_cell):
                    continue

                new_chain = placement_chain.copy()
                new_chain.add(new_cell)
                deeper_chains = self._search(new_chain, remaining_search_size - 1)

                search_result.update(deeper_chains)

        return search_result

    def get_all_possible_placements(self):
        """
        Obtain all the possible placements.
        The color for the test is automatically determined from the current board status.
        """
        results = set()
        initiatable_cells = self._get_initiatable_cells()

        for chain_size in range(3, 6):
            if not self._is_source_in_hand((-1,) * chain_size):
                continue

            for cell in initiatable_cells:
                placements = self._search({(cell[0], cell[1])}, chain_size - 1)
                results.update(placements)

        return results

    def get_board(self):
        """Obtain the board instance"""
        return self._board
