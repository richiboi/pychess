"""
Board class to represent everything board related.
Only a container for pieces. Can first setup a board given
a config file.
Also has function to perform a move. Should have helper function
to get back a list of all moves possible (for potential AI)
Does not keep track of turn.
"""

from piece import Pawn, Rook, Knight, Bishop, Queen, King


class Board():
    def __init__(self, sq_size, config_file):
        self.piece_list = []

        self.sq_size = sq_size
        self.setup_pieces(config_file)

    # Performs the initial setup of pieces from a txt config file
    # Edits the piece_list member variable
    def setup_pieces(self, config_file):
        with open(config_file) as file:
            data = file.read().split('\n')
            data = [line.split(' ') for line in data]
            for r in range(8):
                for c in range(8):
                    if data[r][c] == 'xx':
                        continue

                    args = [(c, r), data[r][c], data[r][c][0] == 'w']
                    piece_type_switcher = {
                        'p': Pawn(*args),
                        'r': Rook(*args),
                        'h': Knight(*args),
                        'b': Bishop(*args),
                        'q': Queen(*args),
                        'k': King(*args)
                    }
                    self.piece_list.append(piece_type_switcher[data[r][c][1]])

    # Function to perform a move. Updates the board's piecelist
    def perform_move(self, move):

        # Set piece's first move to false
        move.piece.first_move = False

        # If there is capture, perform it
        if move.capture:
            self.piece_list.remove(move.capture)

        # Move the piece in question
        move.piece.pos = move.dest

    # Returns the move list for all pieces
    def get_moves(self):
        moves = []

        for piece in self.piece_list:
            moves += piece.get_moves(self.piece_list)

        return moves

    # Returns the move list for a given color
    def get_moves_of_color(self, is_white):
        moves = []

        for piece in self.piece_list:
            if piece.is_white == is_white:
                moves += piece.get_moves(self.piece_list)

        return moves

    def get_moves_of_color_capture_priority(self, is_white):
        moves = []

        for piece in self.piece_list:
            if piece.is_white == is_white:
                moves += piece.get_moves(self.piece_list)

        for piece in self.piece_list:
            if piece.is_white == is_white:
                moves += piece.get_moves(self.piece_list)
