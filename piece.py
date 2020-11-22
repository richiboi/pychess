"""
Contains implementation for a Piece object
Each piece object has a position and a list of moves.
Each piece also has a value
"""

from pos_funcs import pos_add, is_in_bounds
from move import Move


class Piece():
    def __init__(self, pos, piece_type, is_white):
        self.pos = pos  # Tuple (x, y)
        self.is_white = is_white  # Bool
        self.type = piece_type
        self.first_move = True

    # Help with printing out the piece
    def __repr__(self):
        color = 'white' if self.is_white else 'black'
        return f'Type: {self.type}, Position: {self.pos}, color: {color}\n'

    # This method gets linear possible squares. Useful for rook, queen, bishop
    # Takes in a list of all pieces on board, horzvert and diagonal are bools
    # indicating whether to search that direction
    # Returns a list of move objects
    def get_possible_moves_linear(self, piece_list, horzvert, diagonal):
        # Set up search_directions
        moves = []
        search_directions = []

        if horzvert:
            search_directions.extend([(1, 0), (0, 1), (-1, 0), (0, -1)])
        if diagonal:
            search_directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        for search_direction in search_directions:
            self.__search_till_blocked(
                pos_add(self.pos, search_direction), search_direction, piece_list, moves)

        return moves

    # Recursive helper function for get_possible_moves_linear
    # Searches in one particular direction until a path is blocked
    # Adds to a list of move objects (passed in by reference)
    def __search_till_blocked(self, curr_pos, search_direction, piece_list, moves):

        # Base case 1: No longer in bound
        if not is_in_bounds(curr_pos):
            return

        # Base case 2: Another piece is reached
        for piece in piece_list:
            if curr_pos == piece.pos:
                # If different color, append as a capture move
                if piece.is_white != self.is_white:
                    moves.append(Move(self, curr_pos, piece))
                return

        # Otherwise append this and call on the next position
        moves.append(Move(self, curr_pos))
        return self.__search_till_blocked(pos_add(curr_pos, search_direction),
                                          search_direction, piece_list, moves)

    # Used for single square directional movement. King and Knight.
    # Directions is a list of all possible directions (should be 8).
    # Returns a list of possible moves.
    def get_possible_moves_directional(self, piece_list, directions):
        moves = []

        squares_to_check = [pos_add(dir, self.pos) for dir in directions]

        for sq in squares_to_check:
            # If square is not in bound, move on
            if not is_in_bounds(sq):
                continue

            # Now check if there is existing piece of same color
            # TODO: Replace with list comprehension
            for piece in piece_list:
                # If has existing piece
                if sq == piece.pos:
                    # If that piece same color, reject, otherwise add as capture
                    if piece.is_white == self.is_white:
                        break
                    else:
                        moves.append(Move(self, sq, piece))
                        break
            else:
                moves.append(Move(self, sq))

        return moves

    # Function to get back all the possible moves of this piece
    # TODO: Need to implement king filtering
    def get_moves(self, board, check_legality):
        return self.get_possible_moves(board, check_legality)


class Pawn(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 100
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    # TODO: implement en passant
    # Can move two squares forward on its first turn
    # Otherwise, can only move one. Cannot capture in front.
    # Captures via diagonal up or down
    def get_possible_moves(self, board, check_legality):
        piece_list = board.piece_list
        moves = []
        updown = -1 if self.is_white else 1  # Determines the direction based on color

        # Check for diagonal captures
        for piece in piece_list:
            if (piece.pos == pos_add(self.pos, (1, updown)) or piece.pos == pos_add(self.pos, (-1, updown))) and piece.is_white != self.is_white:
                moves.append(Move(self, piece.pos, piece))  # Capture

        sq_ahead_blocked = True

        # Check if square ahead is blocked. Matters for all turns
        # If not, add square ahead to possible moves
        # Doesn't matter what color it is, as it can't capture ahead
        if not pos_add(self.pos, (0, updown)) in [piece.pos for piece in piece_list]:
            sq_ahead_blocked = False
            moves.append(Move(self, pos_add(self.pos, (0, updown))))

        # If first move, and the first square wasn't blocked, check the second square
        if not sq_ahead_blocked and self.first_move:
            if not pos_add(self.pos, (0, updown * 2)) in [piece.pos for piece in piece_list]:
                moves.append(Move(self, pos_add(self.pos, (0, updown * 2))))

        return moves


class Rook(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 500
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_linear(board.piece_list, True, False)


class Knight(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 320
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_directional(board.piece_list, [(2, 1), (2, -1), (1, 2), (1, -2),
                                                                      (-1, 2), (-1, -2), (-2, 1), (-2, -1)])


class Bishop(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 330
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_linear(board.piece_list, False, True)


class Queen(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 9
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_linear(board.piece_list, True, True)


class King(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 20000
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, board, check_legality):
        # Get 8 directional moves
        moves = self.get_possible_moves_directional(board.piece_list, [(1, 1), (1, 0), (1, -1), (0, 1),
                                                                       (0, -1), (-1, 1), (-1, 0), (-1, -1)])

        # If not using king danger squares to check legality moves (if called
        # by a king itself that wants to check for legality), then don't
        # filter through moves
        if not check_legality:
            return moves

        # Filter through all 8 moves - check with king danger squares
        # Condition: if move dest on bitboard is a 0
        king_danger_squares = generate_king_danger_squares(board, self)
        moves = [
            move for move in moves if not king_danger_squares.get(move.dest)]

        return moves


# Function returns a bit board of all king danger squares of a color
def generate_king_danger_squares(board, king):
    bitboard = BitBoard()

    # Remove the current king for now
    board.piece_list.remove(king)

    moves = board.get_moves_of_color(not king.is_white, False)

    for move in moves:
        bitboard.set(move.dest, 1)

    # Restore the king
    board.piece_list.append(king)

    return bitboard


class BitBoard():
    def __init__(self):
        self.data = [0] * 64

    def set(self, pos, val):
        # Takes in a pos tuple (x, y) and a value to set (0 or 1)
        x, y = pos
        self.data[x + y * 8] = val

    def get(self, pos):
        x, y = pos
        return self.data[x + y * 8]
