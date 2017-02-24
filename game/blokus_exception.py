class InvalidPlacementError (Exception):
    """The exception represents an invalid placement on the blokus board."""

    def __init__(self, blokus_board_state, blokus_placement):
        self.blokus_board_state = blokus_board_state
        self.blokus_placement = blokus_placement

    def __str__(self):
        return ("Movement {0} is invalid with the board state\n{1}".format(self.blokus_placement, self.blokus_placement))
