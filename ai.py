"""
Centers around a singular ai_move() function
that returns the given move that is most beneficial
"""

from piece_square_value import get_value_of_position

MINIMAX_DEPTH = 3


# Main recursive function that evaluates the best move.
# Returns a Move object that is the desired object to move

def get_negamax_move(board, is_white):
    move = __negamax(board, is_white, MINIMAX_DEPTH, MINIMAX_DEPTH)
    return move


# Root case will return a move
# All other cases will return best score
def __negamax(board, is_white, depth, start_depth):
    if depth == 0:
        return board_value(board, is_white)

    max_score = -9999
    best_move = None

    # Get all available moves from this point on
    moves = board.get_moves_of_color(is_white)

    for move in moves:
        # Keep track of original state
        piece_original_pos = move.piece.pos
        piece_original_first_move = move.piece.first_move

        # Perform move.
        board.perform_move(move)

        # Evaluate
        score = -(__negamax(board, not is_white,
                            initial_is_white, depth - 1, start_depth))
        if score > max_score:
            max_score = score
            best_move = move

        # Unperform move
        move.piece.pos = piece_original_pos
        move.piece.first_move = piece_original_first_move
        if move.capture:
            board.piece_list.append(move.capture)

    if depth == start_depth:
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
