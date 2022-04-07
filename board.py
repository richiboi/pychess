"""
Board class to represent everything board related.
Only a container for pieces. Can first setup a board given
a config file.
Also has function to perform a move. Should have helper function
to get back a list of all moves possible (for potential AI)
Does not keep track of turn.
"""

from piece import Pawn, Rook, Knight, Bishop, Queen, King
from pos_funcs import is_in_bounds


class Board():
    def __init__(self, config_file):
        # A dict -> key as position and value as the piece
        self.pieces = {}

        self.setup_pieces(config_file)

    def __check_pos_in_bounds(self, position):
        if not is_in_bounds(position):
            raise Exception(f'Position {position} not in bounds!')

    def __getitem__(self, position):
        self.__check_pos_in_bounds(position)
        return self.pieces.get(position)

    def __setitem__(self, position, piece):
        self.__check_pos_in_bounds(position)
        self.pieces[position] = piece

    def __len__(self):
        return len(self.pieces)

    def __iter__(self):
        return iter(self.pieces.values())

    def pop(self, position):
        self.__check_pos_in_bounds(position)
        return self.pieces.pop(position, None)

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
                    # Add to dict
                    self[(c, r)] = piece_type_switcher[data[r][c][1]]

    def __move_piece_to_position(self, origin, destination):
        # Places the piece from the origin to the destination
        self[destination] = self.pop(origin)

    def perform_move(self, move):
        # Function to perform a move

        # Set piece's first move to false
        move.piece.first_move = False

        # If there is capture, perform it
        if move.capture:
            self.pop(move.dest)

        # Move the piece in question
        self.__move_piece_to_position(move.piece.pos, move.dest)
        move.piece.pos = move.dest

    def undo_move(self, move_state):
        # Takes in a move_state object, of which it restores the state to
        self.__move_piece_to_position(
            move_state.move.piece.pos, move_state.pos)
        move_state.move.piece.pos = move_state.pos
        move_state.move.piece.first_move = move_state.first_move

        # If captured, add it back
        if move_state.move.capture:
            self[move_state.move.capture.pos] = move_state.move.capture

    # Returns the move list for all pieces
    def get_moves(self, check_legality=True):
        moves = []

        for piece in self:
            moves += piece.get_moves(self, check_legality)

        return moves

    # Returns the move list for a given color
    def get_moves_of_color(self, is_white, check_legality=True):
        moves = []

        # TODO: Remove this list(self) type conversion for efficiency
        for piece in list(self):
            if piece.is_white == is_white:
                moves += piece.get_moves(self, check_legality)

        return moves

    def num_pieces_checking_king(self, is_white):
        # Consider if a piece is at the king location
        # Generate all moves for that piece, if there is another piece there,
        # then king is in check
        king = [piece for piece in self if piece.type[1]
                == 'k' and piece.is_white == is_white][0]

        # Consider pawns
        updown = -1 if sis_white else 1  # Determines the direction based on color

        # Consider knight

        # Consider diagonals

        # Consider horz and vert

        return 0

    def search_line_till_blocked(self):
        # Recursively searches in a given direction until blocked
        # Returns the piece object blocking
        pass

# Class that stores the state of a move before
# a move is performed


class MoveState():

    def __init__(self, move):
        self.pos = move.piece.pos
        self.first_move = move.piece.first_move
        self.move = move
