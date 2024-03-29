"""
Handles the drawing of pieces onto the screen and clicks.
Should abstract away the board directly from the player.
Doesn't handle AI Logic but will call the function for
the AI to make a move given the board.

TODO: UPDATE FUNCTIONALITY with the new board dict
"""

from ai import get_ai_move
from pos_funcs import pos_divide_whole, pos_multiply,  pos_add
from board import Board
import pygame
import os
import time

PIECE_SIZE = 1
CIRCLE_SIZE = 0.2


class GameManager():
    def __init__(self, win, sq_size, starter_config_file):
        self.win = win
        self.sq_size = sq_size
        self.selected_piece = None
        self.is_white_turn = True
        self.board = Board(starter_config_file)

        # Current move list keeps track of moves of selected piece
        self.selected_piece_moves = []

    # Main draw function for drawing pieces and move circles
    def draw(self):
        self.__draw_pieces()

        # draw selected piece
        if self.selected_piece:
            self.__draw_circle(self.selected_piece.pos,
                               (255, 0, 0))

            # Draw the moves of the selected piece
            for move in self.selected_piece_moves:
                self.__draw_circle(move.dest, (0, 0, 255))

    # Draws all the pieces onto the board
    def __draw_pieces(self):
        # Loop through all the pieces in the board
        for piece in self.board:
            image = pygame.image.load(os.path.join(
                '128h sprites', piece.type + '.png'))

            image_transformed = pygame.transform.scale(
                image, (int(self.sq_size * PIECE_SIZE), int(self.sq_size * PIECE_SIZE)))

            self.win.blit(
                image_transformed, pos_multiply(piece.pos, self.sq_size))

    # Draws a circle from a center. Takes in a color, and a size (0-1)
    def __draw_circle(self, center, color):
        pygame.draw.circle(self.win, color, pos_multiply(
            pos_add(center, (0.5, 0.5)), self.sq_size), int(self.sq_size * CIRCLE_SIZE))

    # MousePos in (x, y)
    def handle_board_click(self, mouse_pos):
        square_clicked = pos_divide_whole(mouse_pos, self.sq_size)

        # If a piece is selected, check if it clicks on one of the moves
        if self.selected_piece:
            for move in self.selected_piece_moves:
                if square_clicked == move.dest:

                    self.board.perform_move(move)

                    # Deselect
                    self.select_piece(None)

                    # Change to black turn or AI perform move
                    # Also times the AI
                    # self.is_white_turn = not self.is_white_turn

                    start = time.time()
                    ai_move = get_ai_move(
                        self.board, not self.is_white_turn, 4)
                    end = time.time()
                    print('----------------')
                    print(ai_move)
                    print(f'Execution time: {end - start}')
                    self.board.perform_move(ai_move)

                    return

        # If piece is selected and click itself, deselect
        if self.selected_piece and self.selected_piece.pos == square_clicked:
            self.select_piece(None)
            return

        # If another piece is selected and of same color, set it as the new selected piece
        if self.board[square_clicked] and self.board[square_clicked].is_white == self.is_white_turn:
            self.select_piece(self.board[square_clicked])
            return

        # Otherwise, just deselect
        self.select_piece(None)

    # Function to select piece. Also updates the selected_piece_moves
    def select_piece(self, piece):
        self.selected_piece = piece

        if piece:
            self.selected_piece_moves = piece.get_moves(
                self.board, True)
        else:
            self.selected_piece_moves = []
