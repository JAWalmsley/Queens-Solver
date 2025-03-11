from board import Board
import json

def parse_orig(filename: str, board_id: int) -> Board:
    with open(filename, 'r') as file:
        data = json.load(file)
        return Board(data[board_id]['caseNumber'], data[board_id]['colorGrid'])
    
def parse_archivedqueens(filename: str, index: int) -> tuple[int, Board]:
    with open(filename, 'r') as file:
        data = json.load(file)
        board = data[index]
        return (board['id'],Board(len(board['regions'][0]), board['regions']))

def parse_archivedqueens_byID(filename:str, id: int) -> Board:
    with open(filename, 'r') as file:
        data = json.load(file)
        for board in data:
            if board['id'] == id:
                return Board(len(board['regions'][0]), board['regions'])
        raise "Board doesn't exist!"
     
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
