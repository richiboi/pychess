"""
File contains helper functions for dealing with position tuples (x, y)
"""


def is_in_bounds(pos):
    return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7


def pos_add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def pos_multiply(pos, scalar):
    return (pos[0] * scalar, pos[1] * scalar)


def pos_divide_whole(pos, denominator):
    return (pos[0] // denominator, pos[1] // denominator)
