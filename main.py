import pygame
from pygame.constants import MOUSEBUTTONUP
import draw
import pieces as pi


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 179, 149)
BLACK = (0, 0, 0)


# Pygame-stuff
pygame.init()

WIDTH = 704
WIN = pygame.display.set_mode((WIDTH, WIDTH))
running = True
board1 = pi.Board()
board1.set_initial_board(WIDTH)
first_press = True
moving_piece = False
white_to_play = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if pygame.mouse.get_pressed()[0]:
            pos_mouse = pygame.mouse.get_pos()
            if not moving_piece:
                row_pressed, col_pressed = draw.det_pos_on_board(WIDTH, *pos_mouse)
                selected_piece = board1.piece_selected(row_pressed, col_pressed)
            
            if selected_piece is not None:
                moving_piece = True
                selected_piece.update_pos(*pos_mouse)
        
        if event.type == pygame.MOUSEBUTTONUP and moving_piece:
            pos_mouse = event.pos
            row_released, col_released = draw.det_pos_on_board(WIDTH, *pos_mouse)
            piece_at_released = board1.piece_selected(row_released, col_released)
            
            if not isinstance(piece_at_released, pi.Piece):
                if selected_piece.allowed_to_move(row_released, col_released):
                    board1.move_piece(row_pressed, col_pressed, row_released, col_released)
            else:
                if board1.allowed_to_take(row_pressed, col_pressed, row_released, col_released):
                    board1.move_piece(row_pressed, col_pressed, row_released, col_released)
            
            selected_piece.resting_pos(WIDTH)
            moving_piece = False
    
    draw.draw(WIN, WIDTH, board1)
