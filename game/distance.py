import math


def manhattan_2d(start_vec, end_vec):
    """Returns a Manhattan distance between two given points."""
    return math.abs(start_vec[0] - end_vec[0]) + math.abs(start_vec[1] - end_vec[1])


def chebyshev_2d(start_vec, end_vec):
    """Returns a Chebyshev distance between two given points."""
    return max(math.abs(start_vec[0] - end_vec[0]), math.abs(start_vec[1] - end_vec[1]))
