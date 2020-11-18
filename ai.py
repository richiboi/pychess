"""
Centers around a singular ai_move() function
that returns the given move that is most beneficial
"""

MINIMAX_DEPTH = 2

"""
Main recursive function that evaluates the best move.
Returns a Move object that is the desired object to move

"""


def get_minimax_move(board, is_white):
    move, score = __minimax(board, is_white, MINIMAX_DEPTH, None)
    return move


# Returns a node represented by tuple (Move, score)
def __minimax(board, is_white, depth, curr_move):
    if depth == 0:
        return curr_move, board_value(board, is_white)

    max_score = -9999
    best_move = None
    for piece in board.piece_list:
        if piece.is_white != is_white:
            continue

        for move in piece.moves:
            # Keep track of original state
            piece_original_pos = piece.pos
            piece_original_first_move = piece.first_move

            # Perform move. Returns the index of the removed captured piece
            index = ai_perform_move(move, board.piece_list)

            board.update_piece_moves()

            # Evaluate
            move_evaluated, score = __minimax(
                board, not is_white, depth - 1, move)
            if score > max_score:
                max_score = score
                best_move = move_evaluated

            # Unperform move
            piece.pos = piece_original_pos
            piece.first_move = piece_original_first_move
            if move.capture:
                board.piece_list.insert(index, move.capture)

    return best_move, max_score


# Testing function that returns a move based on the board value
def get_ai_move_by_board_value(board, is_white):
    optimum_move = None
    best_score = -9999

    for piece in board.piece_list:

        if piece.is_white != is_white:
            continue

        for move in piece.moves:
            # Keep track of original state
            piece_original_pos = piece.pos
            piece_original_first_move = piece.first_move

            # Perform move. Returns the index of the removed captured piece
            index = ai_perform_move(move, board.piece_list)

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


# Similar to board's perform move only the move list doesn't update
# pieces moves list for efficiency
# Returns the index in the piece_list of the removed captured piece
# to be used for later insertion
def ai_perform_move(move, piece_list):
    # Set piece's first move to false
    move.piece.first_move = False

    # If there is capture, perform it
    index = 0
    if move.capture:
        index = piece_list.index(move.capture)
        piece_list.remove(move.capture)

    # Move the piece in question
    move.piece.pos = move.dest
    return index


# Function to evaluate the value of a given board
# Pieces with a different is_white is given a negative value
# Returns an integer representing the value of the board
def board_value(board, is_white):
    value = 0
    for piece in board.piece_list:
        value += piece.value * (1 if piece.is_white == is_white else -1)

    return value
