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
        return f'{self.type} at {self.pos}'

    # This method gets linear possible squares. Useful for rook, queen, bishop
    # Takes in a list of all pieces on board, horzvert and diagonal are bools
    # indicating whether to search that direction
    # Returns a list of move objects
    def get_possible_moves_linear(self, board, horzvert, diagonal):
        # Set up search_directions
        moves = []
        search_directions = []

        if horzvert:
            search_directions.extend([(1, 0), (0, 1), (-1, 0), (0, -1)])
        if diagonal:
            search_directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        # Perform search for each direction
        for search_direction in search_directions:
            self.__search_till_blocked(
                pos_add(self.pos, search_direction), search_direction, board, moves)

        return moves

    # Recursive helper function for get_possible_moves_linear
    # Searches in one particular direction until a path is blocked
    # Adds to a list of move objects (passed in by reference)
    def __search_till_blocked(self, curr_pos, search_direction, board, moves):

        # Base case 1: No longer in bound
        if not is_in_bounds(curr_pos):
            return

        # Base case 2: Another piece is reached
        if board[curr_pos]:
            # If different color, append as a capture move
            if board[curr_pos].is_white != self.is_white:
                moves.append(Move(self, curr_pos, board[curr_pos]))
            return

        # Otherwise append this and call on the next position
        moves.append(Move(self, curr_pos))
        return self.__search_till_blocked(pos_add(curr_pos, search_direction),
                                          search_direction, board, moves)

    # Used for single square directional movement. King and Knight.
    # Directions is a list of all possible directions (should be 8).
    # Returns a list of possible moves.
    def get_possible_moves_directional(self, board, directions):
        moves = []

        # List Comprehension! Only add if in bounds
        squares_to_check = [pos_add(
            dir, self.pos) for dir in directions if is_in_bounds(pos_add(dir, self.pos))]

        for square in squares_to_check:
            # If no piece there, add
            if not board[square]:
                moves.append(Move(self, square))
            elif board[square].is_white != self.is_white:
                moves.append(Move(self, square, board[square]))  # Capture

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
        moves = []
        updown = -1 if self.is_white else 1  # Determines the direction based on color

        # Check for diagonal captures - loop through left and right
        for diagonal_sq in [pos_add(self.pos, (1, updown)), pos_add(self.pos, (-1, updown))]:
            if is_in_bounds(diagonal_sq) and board[diagonal_sq] and board[diagonal_sq].is_white != self.is_white:
                moves.append(
                    Move(self, diagonal_sq, board[diagonal_sq]))  # Capture

        # If one ahead isn't blocked, then add one ahead.
        # Then if two ahead isn't blocked and it's first turn, add it
        one_ahead = pos_add(self.pos, (0, updown))
        if not board[one_ahead]:
            moves.append(Move(self, one_ahead))

            two_ahead = pos_add(self.pos, (0, updown * 2))
            if self.first_move and not board[two_ahead]:
                moves.append(Move(self, two_ahead))

        return moves


class Rook(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 500
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a board
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_linear(board, True, False)


class Knight(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 320
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a board
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_directional(board, [(2, 1), (2, -1), (1, 2), (1, -2),
                                                           (-1, 2), (-1, -2), (-2, 1), (-2, -1)])


class Bishop(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 330
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a board
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_linear(board, False, True)


class Queen(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 9
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a board
    def get_possible_moves(self, board, check_legality):
        return self.get_possible_moves_linear(board, True, True)


class King(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 20000
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, board, check_legality):
        # Get 8 directional moves
        moves = self.get_possible_moves_directional(board, [(1, 1), (1, 0), (1, -1), (0, 1),
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
            move for move in moves if not king_danger_squares[move.dest]]

        return moves


# Function returns a bit board of all king danger squares of a color
def generate_king_danger_squares(board, king):
    king_danger_squares = BitBoard()

    # Remove the current king for now
    board.pop(king.pos)

    moves = board.get_moves_of_color(not king.is_white, False)

    for move in moves:
        king_danger_squares[move.dest] = 1

    # Restore the king
    board[king.pos] = king

    return king_danger_squares


class BitBoard():
    def __init__(self):
        self.data = [0] * 64

    def __getitem__(self, position):
        x, y = position
        return self.data[x + y * 8]

    def __setitem__(self, position, value):
        # Takes in a pos tuple (x, y) and a value to set (0 or 1)
        x, y = position
        self.data[x + y * 8] = value
