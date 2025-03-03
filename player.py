from board import Board
import itertools
from collections import Counter

class Player:
    def __init__(self):
        pass
    def get_blocked_coords(self, board: Board, x, y):
        out = set()
        for i in range(board.size):
            if i != x:
                out.add((i, y))
        for i in range(board.size):
            if i!=y:
                out.add((x,i))
        out.add((x-1, y))
        out.add((x+1, y))
        out.add((x-1, y+1))
        out.add((x+1, y+1))
        out.add((x+1, y-1))
        out.add((x-1, y-1))
        return out
    
    def block_overlap_positions(self, board: Board, regions: dict[int, set]):
        """
        Block any positions that are blocked by every spot in a region
        """
        # Find smallest region
        region_sizes = {region: len(spots) for region, spots in regions.items()}
        sorted_regions = sorted(region_sizes, key=region_sizes.get)
        for curr_region in sorted_regions:
            # Try each position in that region
            blocked = []
            for row in range(board.size):
                for col in range(board.size):
                    if board.colours[row][col] == curr_region and (col,row) not in board.markers and (col,row) not in board.queens:
                        blocked.append(self.get_blocked_coords(board, col, row))
            if len(blocked) > 0:
                # Mark squares in overlap of those blocked regions
                common_blocked = set.intersection(*blocked)

                for pos in common_blocked:
                    board.add_marker(pos[0], pos[1])
    
    def place_in_last_slot(self, board: Board, regions: dict[int, set]):
        """
        Place a queen if there is only one spot left in a region
        """
        for region, spots in regions.items():
            free_spots: set = spots.difference(board.markers)
            free_spots = free_spots.difference(board.queens)
            if len(free_spots) == 1:
                board.add_queen(*(free_spots.pop()))

    def next_move(self, curr_board: Board):
        board = curr_board.copy()
        regions = {}
        for row in range(board.size):
            for col in range(board.size):
                regions[board.colours[row][col]] = set()
        for row in range(board.size):
            for col in range(board.size):
                if (col,row) not in board.queens and (col,row) not in board.markers:
                    regions[board.colours[row][col]].add((col, row))
        self.block_overlap_positions(board, regions)
        self.place_in_last_slot(board, regions)
        return board