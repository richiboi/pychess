"""
Contains implementation for a Move object

"""


class Move():
    def __init__(self, piece, dest, capture=None, promotion=None):
        self.piece = piece      # Piece object - the piece we want to move
        self.dest = dest        # Tuple (x, y) - Destination of the piece

        # Piece object - the piece we want to capture (delete)
        self.capture = capture

        # Promotion - the new piece we want to promote it to

    def __repr__(self):
        return f'Piece: {self.piece} \nDestination: {self.dest} \nCapture: {self.capture}'
