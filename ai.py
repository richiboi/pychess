"""
Centers around a singular ai_move() function
that returns the given move that is most beneficial
"""

from piece_square_value import get_value_of_position

MINIMAX_DEPTH = 4


# Main recursive function that evaluates the best move.
# Returns a Move object that is the desired object to move

def get_ai_move(board, is_white, depth):
    move = __negamax(board, -99999, 99999, is_white,
                     depth, depth)
    return move


# Root case will return a move
# All other cases will return best score
def __negamax(board, alpha, beta, is_white, depth, start_depth):
    if depth == 0:
        return board_value(board, is_white)

    max_score = -99999
    best_move = None

    # Get all available moves from this point on
    moves = board.get_moves_of_color(is_white)

    for move in moves:
        # Keep track of original state
        move_state = MoveState(move)

        # Perform move
        board.perform_move(move)

        # Get score
        score = -(__negamax(board, -beta, -alpha,
                            not is_white, depth - 1, start_depth))

        # Unperform move
        move_state.undo_move(board)

        # Evaluate
        if score > max_score:
            max_score = score
            best_move = move

        alpha = max(alpha, score)

        if alpha >= beta:
            break

    if depth == start_depth:
        print(max_score)
        return best_move
    else:
        return max_score


# Function to evaluate the value of a given board
# Pieces with a different is_white is given a negative value
# Returns an integer representing the value of the board
def board_value(board, is_white):
    value = 0
    for piece in board.piece_list:
        multiplier = 1 if piece.is_white == is_white else -1
        value += piece.value * multiplier            # Add piece value
        # Add position value
        value += get_value_of_position(piece.pos, piece.type) * multiplier

    return value


# Testing function that returns a move based on the board value
def get_ai_move_by_board_value(board, is_white):
    optimum_move = None
    best_score = -9999

    # Get all available moves from this point on
    moves = board.get_moves_of_color(is_white)

    for move in moves:
        # Keep track of original state
        piece_original_pos = piece.pos
        piece_original_first_move = piece.first_move

        if move.capture:
            captured_piece = move.capture
            captured_piece_index = board.piece_list.index(move.capture)

        # Perform move.
        board.perform_move(move)

        # Evaluate
        board_score = board_value(board, is_white)
        if board_score > best_score:
            optimum_move = move
            best_score = board_score

        # Unperform move
        piece.pos = piece_original_pos
        piece.first_move = piece_original_first_move
        if move.capture:
            board.piece_list.insert(index, move.capture)

    return optimum_move


# Class that stores the state of a move before
# a move is performed
class MoveState():

    def __init__(self, move):
        self.pos = move.piece.pos
        self.first_move = move.piece.first_move
        self.move = move

    def undo_move(self, board):
        self.move.piece.pos = self.pos
        self.move.piece.first_move = self.first_move
        if self.move.capture:
            board.piece_list.append(self.move.capture)
