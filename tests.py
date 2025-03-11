import pygame
import unittest
import json
import time
from board import Board
from player import Player
import map_parse

# Define constants
WINDOW_SIZE = 500

file_path = 'maps.json'     

curr_map = {}



# Initialize pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Queens Game")

def draw_game(curr_map):
    if curr_map.is_complete():
        background = "green"
    else:
        background = "black"
    screen.fill(background)
    curr_map.draw(screen)
    pygame.display.flip()

class TestGame(unittest.TestCase):
    def helper_test_board(self, curr_map):
        p = Player()
        iters = 0
        while not curr_map.is_complete():
            curr_map = p.next_move(curr_map)
            self.assertTrue(curr_map.is_valid())
            # draw_game(curr_map)
            iters += 1
            if iters > 20:
                self.fail("Timeout, made too many moves without finishing")
            # time.sleep(0.05)
        # time.sleep(0.5)
    
    def test_one(self):
        self.helper_test_board(1)
    
    def test_four(self):
        self.helper_test_board(4)
    
    def test_all(self):
        for i in range(1,100):
            with self.subTest(id=f"{i:02}"):
                board = map_parse.parse_orig(file_path, id)
                self.helper_test_board(board)
            
    def test_archive(self):
        for i in range(139):
            id, board = map_parse.parse_archivedqueens("archivedqueens.json", i)
            with self.subTest(id=f"{id:03}"):
                self.helper_test_board(board)