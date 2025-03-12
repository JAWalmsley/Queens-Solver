import pygame
import colorsys
import copy
LINE_THICKNESS = 4

MAX_REGIONS = 10
HSV_tuples = [(x/MAX_REGIONS, 0.6, 1.0) for x in range(MAX_REGIONS)]
COLOURS = [tuple(i*255 for i in colorsys.hsv_to_rgb(*x)) for x in HSV_tuples]
PADDING = 10



class Board:
    def __init__(self, size, board):
        self.size = size
        self.colours = board
        self.queens = set()
        self.markers = set()
        
        self.fix_board_region_numbers()
    
    def __eq__(self, other):
        return self.size == other.size\
            and self.colours == other.colours\
            and self.queens == other.queens\
            and self.markers == other.markers
    
    def fix_board_region_numbers(self):
        # The board should be from 0 to N-1, sometimes they skip random numbers in between for some reason
        existing_nums = set([cell for row in self.colours for cell in row])
        expected_nums = {i for i in range(self.size)}
        missing_nums = expected_nums.difference(existing_nums)
        unexpected_nums = existing_nums.difference(expected_nums)
        for old, new in zip(unexpected_nums, missing_nums):
            for row in self.colours:
                for i,val in enumerate(row):
                    if val == old:
                        row[i] = new
        pass
    
    def reset(self):
        self.queens = set()
        self.markers = set()

    def copy(self):
        b = copy.deepcopy(self)
        return b

    def draw(self, screen: pygame.Surface):
        square_size = screen.get_size()[0]/self.size
        for row in range(self.size):
            for col in range(self.size):
                pygame.draw.rect(screen, COLOURS[self.colours[row][col]], (col * square_size+LINE_THICKNESS/2, row * square_size+LINE_THICKNESS/2, square_size-LINE_THICKNESS, square_size-LINE_THICKNESS))
        for (col, row) in self.queens:
            pygame.draw.circle(screen,"black", (col * square_size+square_size/2, row * square_size+square_size/2), square_size/2 - PADDING, 4)
        for (col,row) in self.markers:
            pygame.draw.line(screen, "black", (col * square_size + PADDING, row * square_size + PADDING), ((col+1) * square_size - PADDING, (row+1) * square_size - PADDING), 5)
            pygame.draw.line(screen, "black", ((col+1) * square_size - PADDING, row * square_size + PADDING), ((col) * square_size + PADDING, (row+1) * square_size - PADDING), 5)

    def add_queen(self, x, y):
        if x >= self.size or y >= self.size:
            return
        if (x,y) in self.markers:
            return
        else:
            self.queens.add((x,y))
            self.auto_mark(x, y)
    def remove_queen(self, x, y):
        if x >= self.size or y >= self.size:
            return
        if (x,y) in self.queens:
            self.queens.remove((x,y))

    def auto_mark(self, x, y):
        for i in range(self.size):
            if i != x:
                self.add_marker(i, y)
        for i in range(self.size):
            if i!=y:
                self.add_marker(x,i)
        self.add_marker(x-1, y)
        self.add_marker(x+1, y)
        self.add_marker(x-1, y+1)
        self.add_marker(x+1, y+1)
        self.add_marker(x+1, y-1)
        self.add_marker(x+1, y-1)
        self.add_marker(x-1, y-1)
        colour = self.colours[y][x]
        for row in range(self.size):
            for col in range(self.size):
                if self.colours[row][col] == colour:
                    self.add_marker(col, row)

    def add_marker(self, x, y):
        if x >= self.size or y >= self.size:
            return
        if (x,y) in self.queens:
            return
        else:
                self.markers.add((x,y))

    def remove_marker(self, x, y):
        if x >= self.size or y >= self.size:
            return
        if (x,y) in self.markers:
            self.markers.remove((x,y))
    
    def is_empty(self, x, y):
        if (x,y) in self.queens or (x,y) in self.markers:
            return False
        return True

    def is_valid(self):
        # Regions (colours) queen count
        colour_region_queens = [0 for i in range(self.size)]
        for q1 in self.queens:
            # Increment number of queens in this queen's colour
            colour_region_queens[self.colours[q1[1]][q1[0]]] += 1
            for q2 in self.queens:
                if q1 == q2:
                    continue
                # Same X
                if q1[0] == q2[0]:
                    return False
                # Same y
                if q1[1] == q2[1]:
                    return False
                # Corners
                if abs(q1[0]-q2[0]) == 1 and abs(q1[1]-q2[1]) == 1:
                    return False
        # No more than one queen per colour region
        for region in colour_region_queens:
            if region > 1:
                return False
        return True

    def is_complete(self):
        return self.is_valid() and len(self.queens) == self.size