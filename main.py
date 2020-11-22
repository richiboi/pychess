"""
Entry point of the entire program.
Contains function to draw the checkerboard onto the screen.
Does not draw pieces however.
Only for very basic event loop.

Any board position is stored as tuple (x, y)
X goes left to right
Y goes top to bottom
"""

import pygame
from game_manager import GameManager

SQ_SIZE = 60
CONFIG_FILE = "board_configs/super_simple.txt"

# Initializing pygame stuff
pygame.init()
win = pygame.display.set_mode((SQ_SIZE * 8, SQ_SIZE * 8))
pygame.display.set_caption("pychess")
clock = pygame.time.Clock()


# Initialize gameManager
gm = GameManager(win, SQ_SIZE, CONFIG_FILE)


# Function to draw the checkerboard onto pygame
def draw_checkerboard():
    for c in range(8):
        for r in range(8):
            color = (222, 184, 135) if (c+r) % 2 == 0 else (133, 69, 19)
            pygame.draw.rect(
                win, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Main event loop
run = True
while run:
    clock.tick(60)  # Make it 60fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            gm.handle_board_click(pygame.mouse.get_pos())

    draw_checkerboard()
    gm.draw()
    pygame.display.update()

pygame.quit()
