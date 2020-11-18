"""
Contains implementation for a Piece object
Each piece object has a position and a list of moves.
"""

from pos_funcs import pos_add, is_in_bounds
from move import Move


class Piece():
    def __init__(self, pos, piece_type, is_white):
        self.pos = pos  # Tuple (x, y)
        self.is_white = is_white  # Bool
        self.moves = []  # A list of move objects
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
            else:
                moves.append(Move(self, sq))

        return moves

    # Function to update the member variable moves list
    # Will filter out if king is put into danger or not
    def update_moves(self, piece_list):
        self.moves = self.get_possible_moves(piece_list)


class Pawn(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 1
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    # TODO: implement en passant
    # Can move two squares forward on its first turn
    # Otherwise, can only move one. Cannot capture in front.
    # Captures via diagonal up or down
    def get_possible_moves(self, piece_list):
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
        self.value = 5
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, piece_list):
        return self.get_possible_moves_linear(piece_list, True, False)


class Knight(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 3
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, piece_list):
        return self.get_possible_moves_directional(piece_list, [(2, 1), (2, -1), (1, 2), (1, -2),
                                                                (-1, 2), (-1, -2), (-2, 1), (-2, -1)])


class Bishop(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 3
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, piece_list):
        return self.get_possible_moves_linear(piece_list, False, True)


class Queen(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 9
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, piece_list):
        return self.get_possible_moves_linear(piece_list, True, True)


class King(Piece):
    def __init__(self, pos, type, is_white):
        self.value = 9000
        super().__init__(pos, type, is_white)

    # Function returns a list of possible moves given a piece_list
    def get_possible_moves(self, piece_list):
        return self.get_possible_moves_directional(piece_list, [(1, 1), (1, 0), (1, -1), (0, 1),
                                                                (0, -1), (-1, 1), (-1, 0), (-1, -1)])
