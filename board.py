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
        self.piece_list = []  # Stores as a list of pieces
        self.pos_piece_dict = {}  # Stores as a map - pos tuple -> piece

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
                    # Add to list
                    piece = piece_type_switcher[data[r][c][1]]
                    self.piece_list.append(piece)

                    # Add to dict
                    self.pos_piece_dict[(c, r)] = piece

    def perform_move(self, move):
        # Function to perform a move. Updates the board's piecelist and dict

        # Set piece's first move to false
        move.piece.first_move = False

        # If there is capture, perform it
        if move.capture:
            self.piece_list.remove(move.capture)
            self.pos_piece_dict.pop(move.piece.pos)

        # Move the piece in question
        move.piece.pos = move.dest

    def undo_move(self, move_state):
        # Takes in a move_state object, of which it restores the state to
        move_state.move.piece.pos = move_state.pos
        move_state.move.piece.first_move = move_state.first_move

        if move_state.move.capture:
            self.piece_list.append(move_state.move.capture)
            self.pos_piece_dict[move_state.pos] = move_state.move.piece

    # Returns the move list for all pieces
    def get_moves(self, check_legality=True):
        moves = []

        for piece in self.piece_list:
            moves += piece.get_moves(self, check_legality)

        return moves

    # Returns the move list for a given color
    def get_moves_of_color(self, is_white, check_legality=True):
        moves = []

        for piece in self.piece_list:
            if piece.is_white == is_white:
                moves += piece.get_moves(self, check_legality)

        return moves

    def num_pieces_checking_king(self, is_white):
        # Consider if a piece is at the king location
        # Generate all moves for that piece, if there is another piece there,
        # then king is in check
        king = [piece for piece in self.piece_list if piece.type[1]
                == 'k' and piece.is_white == is_white][0]

        # Create a dictionary that maps positions to pieces without kings
        pos_piece_dict = self.create_pos_piece_dict(is_white)

        # Consider pawns

        # Consider knight

        # Consider diagonals

        # Consider horz and vert

        return 0

    def search_till_blocked(self):
        pass


# Class that stores the state of a move before
# a move is performed
class MoveState():

    def __init__(self, move):
        self.pos = move.piece.pos
        self.first_move = move.piece.first_move
        self.move = move
