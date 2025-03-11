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
    
    def block_overlap_positions(self, board: Board, regions: list[set]):
        """
        Block any positions that are blocked by every spot in a region
        """
        for curr_region_positions in regions:
            # Try each position in that region
            blocked = []
            for pos in curr_region_positions:
                    if pos not in board.markers and pos not in board.queens:
                        blocked.append(self.get_blocked_coords(board,pos[0], pos[1]))
            if len(blocked) > 0:
                # Mark squares in overlap of those blocked regions
                common_blocked = set.intersection(*blocked)

                for pos in common_blocked:
                    board.add_marker(pos[0], pos[1])
    
    def pairs_in_rows(self, board: Board, regions: list[set]):
        for r1 in regions:
            r1_x_set = {pos[0] for pos in r1}
            r1_y_set = {pos[1] for pos in r1}
            for r2 in regions:
                r2_x_set = {pos[0] for pos in r2}
                r2_y_set = {pos[1] for pos in r2}
                if r1 == r2:
                    continue
                if r1_x_set == r2_x_set and len(r1_x_set) == 2:
                    # block every square in those rows not part of these regions
                    for x in r1_x_set:
                        for y in range(board.size):
                            if (x,y) not in r1 and (x,y) not in r2:
                                board.add_marker(x, y)
                if r1_y_set == r2_y_set and len(r1_y_set) == 2:
                    # block every square in those cols not part of these regions
                    for x in  range(board.size):
                        for y in r1_y_set:
                            if (x,y) not in r1 and (x,y) not in r2:
                                board.add_marker(x, y)

    
    def place_in_last_slot(self, board: Board, regions: list[set]):
        """
        Place a queen if there is only one spot left in a region
        """
        for spots in regions:
            free_spots: set = spots.difference(board.markers)
            free_spots = free_spots.difference(board.queens)
            if len(free_spots) == 1:
                board.add_queen(*(free_spots.pop()))

    def next_move(self, curr_board: Board):
        board = curr_board.copy()
        region_dict = {}
        for row in range(board.size):
            for col in range(board.size):
                region_dict[board.colours[row][col]] = set()
        for row in range(board.size):
            for col in range(board.size):
                if (col,row) not in board.queens and (col,row) not in board.markers:
                    region_dict[board.colours[row][col]].add((col, row))

        region_list = list(region_dict.values())
        rows = [{(x,y) for x in range(board.size)} for y in range(board.size)]
        cols = [{(x,y) for y in range(board.size)} for x in range(board.size)]

        regions_and_cols_rows = region_list + cols + rows
        # Block spots that are blocked by every potential queen in a region
        self.block_overlap_positions(board, regions_and_cols_rows)
        # Place a queen if there is only one unblocked slot left in a region
        self.place_in_last_slot(board, regions_and_cols_rows)

        self.pairs_in_rows(board, region_list)
        
        # If the board didn't change we didn't find anything better... Pick a random slot?
        # if board == curr_board:
        #     for r in region_list:
        #         if len(r) > 0:
        #             board.add_queen(*(list(r)[0]))
        #             break
        return board