from board import Board
import json
import requests
from datetime import datetime

def parse_orig(filename: str, board_id: int) -> Board:
    with open(filename, 'r') as file:
        data = json.load(file)
        return Board(data[board_id]['caseNumber'], data[board_id]['colorGrid'])

def get_num_boards(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
        return len(data)

class ArchivedQueensParser:
    def __init__(self, filename, check_update=False):
        with open(filename, 'r') as file:
            self.data = json.load(file)
            if check_update and datetime.strptime(self.data[0]['date'], "%Y/%m/%d").date() < datetime.today().date():
                print("No game for today's date, updating archive")
                req = requests.get("https://queensstorage.blob.core.windows.net/puzzles/linkedinPuzzles.json")
                if req.status_code == 200:
                    self.data = req.json()
                    for index, board in enumerate(self.data):
                        if board['id'] == 177:
                            board['regions'][6][7] = 9
                            board['regions'][6][8] = 9
                            board['regions'][7][7] = 9
                            board['regions'][7][8] = 9
                    with open("archivedqueens.json", 'w') as f:
                        f.write(json.dumps(self.data))
    
    def getNumBoards(self):
        return len(self.data)
    
    def getByID(self, id):
        for board in self.data:
            if board['id'] == id:
                return Board(len(board['regions'][0]), board['regions'])
        raise "Board doesn't exist!"

    def getByIndex(self, index):
        board = self.data[index]
        return (board['id'],Board(len(board['regions'][0]), board['regions']))

# def parse_archivedqueens(filename: str, index: int) -> tuple[int, Board]:
#     with open(filename, 'r') as file:
#         data = json.load(file)
#         if datetime.strptime(data[0]['date'], "%Y/%m/%d").date() < datetime.today().date():
#             update_archive()
#             data = json.load(file)
#         board = data[index]
#         return (board['id'],Board(len(board['regions'][0]), board['regions']))

# def parse_archivedqueens_byID(filename:str, id: int) -> Board:
#     with open(filename, 'r') as file:
#         data = json.load(file)
#         if datetime.strptime(data[0]['date'], "%Y/%m/%d").date() < datetime.today().date():
#             update_archive()
#         for board in data:
#             if board['id'] == id:
#                 return Board(len(board['regions'][0]), board['regions'])
#         raise "Board doesn't exist!"
     
if __name__ == '__main__':
    id, board = parse_archivedqueens('archivedqueens.json', 1)
    import pygame
    print(id)
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Queens Game")
    screen.fill((0,0,0))
    board.draw(screen)
    pygame.display.flip()
    pass
    # import main
    # main.draw_game(board)
