"""
Contains implementation for a Move object
The move object only acts as a struct to store properties for a move
"""


class Move():
    def __init__(self, piece, dest, capture=None):
        self.piece = piece      # Piece object - the piece we want to move
        self.dest = dest        # Tuple (x, y) - Destination of the piece

        # Piece object - the piece we want to capture (delete)
        self.capture = capture
