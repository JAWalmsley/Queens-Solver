import pygame
import sys
import json
import colorsys
from board import Board
from player import Player
import map_parse

# Define constants
WINDOW_SIZE = 500

file_path = 'maps.json'     

# curr_map = map_parse.parse_orig(file_path, 4)
curr_map = map_parse.parse_archivedqueens_byID('archivedqueens.json', 151)

# Initialize pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Queens Game")

def draw_game():
    if curr_map.is_complete():
        background = "green"
    else:
        background = "black"
    screen.fill(background)
    curr_map.draw(screen)
    pygame.display.flip()


background = "black"
dragging = 0
mouse_placing = False
player = Player()
while True:
    draw_game()
    SQUARE_SIZE = WINDOW_SIZE//curr_map.size
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and convert to board coordinates
            dragging = event.button
            x, y = pygame.mouse.get_pos()
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            if curr_map.is_empty(col, row):
                mouse_placing = True
            else:
                mouse_placing = False
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                curr_map = player.next_move(curr_map)
            elif event.key == pygame.K_r:
                curr_map.reset()
        if dragging != 0:
            x, y = pygame.mouse.get_pos()
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE

            # Left click
            if dragging == 1:
                if mouse_placing:
                    curr_map.add_queen(col, row)
                else:
                    curr_map.remove_queen(col, row)
            # Right click
            elif dragging == 3:
                if mouse_placing:
                    curr_map.add_marker(col, row)
                else:
                    curr_map.remove_marker(col, row)