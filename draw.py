import pygame
import pieces as pi


WHITE = (255, 255, 255)
GREEN = (0, 179, 149)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)


def draw_tiles(win, width):
    tile_width = width // 8
    
    for row in range(0,8):
        for col in range(0,8):
            tile_color = WHITE if (row + col) % 2 == 0 else GREEN
            tile_rect = pygame.rect.Rect(col*tile_width, row*tile_width, tile_width, tile_width)
            pygame.draw.rect(win, tile_color, tile_rect)


def draw_pawn(win: pygame.display, pawn):        
    win.blit(pawn.image, (100, 100))


def draw_board(win, board: pi.Board):
    for i in range(8):
        for j in range(8):
            if isinstance(board.board[i][j], pi.Piece):
                board.board[i][j].draw(win)

def draw(win, width, board):
    draw_tiles(win, width)
    draw_board(win, board)

    pygame.display.update()


def det_pos_on_board(width, x, y):
    row = y // (width // 8)
    col = x // (width // 8)
    return row, col