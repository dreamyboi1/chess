import pygame
import os

class Board(object):
    def __init__(self):
        self.board = [
            ["B_R","B_N","B_B","B_Q","B_K","B_B","B_N","B_R"],
            ["B_P","B_P","B_P","B_P","B_P","B_P","B_P","B_P"],
            ["E","E","E","E","E","E","E","E"],
            ["E","E","E","E","E","E","E","E"],
            ["E","E","E","E","E","E","E","E"],
            ["E","E","E","E","E","E","E","E"],
            ["W_P","W_P","W_P","W_P","W_P","W_P","W_P","W_P"],
            ["W_R","W_N","W_B","W_Q","W_K","W_B","W_N","W_R"]
        ]
        self.pawn_board = [
            ["E","E","E","E","E","E","E","E"],
            ["B_P","B_P","B_P","B_P","B_P","B_P","B_P","B_P"],
            ["E","E","E","E","E","E","E","E"],
            ["E","E","E","E","E","E","E","E"],
            ["E","E","E","E","E","E","E","E"],
            ["E","E","E","E","E","E","E","E"],
            ["W_P","W_P","W_P","W_P","W_P","W_P","W_P","W_P"],
            ["E","E","E","E","E","E","E","E"]
        ]
        self.on_board = []
    
    def set_initial_board(self, width):
        self.board = [
            [None, None, None, None, None, None, None, None],
            [Pawn(1,0,"b", width), Pawn(1,1,"b", width), Pawn(1,2,"b", width), Pawn(1,3,"b", width), Pawn(1,4,"b", width), 
             Pawn(1,5,"b", width), Pawn(1,6,"b", width), Pawn(1,7,"b", width)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(6,0,"w", width), Pawn(6,1,"w", width), Pawn(6,2,"w", width), Pawn(6,3,"w", width), Pawn(6,4,"w", width), 
             Pawn(6,5,"w", width), Pawn(6,6,"w", width), Pawn(6,7,"w", width)],
            [None, None, None, None, None, None, None, None],
        ]

        """self.board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, Pawn(1,3,"b",width), None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, Pawn(6,3,"w",width), None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]"""

    def move_piece(self, init_row, init_col, dest_row, dest_col):
        if isinstance(self.board[init_row][init_col], Piece):
            self.board[init_row][init_col].move_to(dest_row, dest_col)
            self.board[dest_row][dest_col] = self.board[init_row][init_col]
            self.board[init_row][init_col] = None

    def piece_selected(self, row, col):
        return self.board[row][col]

    def allowed_to_take(self, init_row, init_col, dest_row, dest_col):
        taking_piece = self.piece_selected(init_row, init_col)
        threatened_piece = self.piece_selected(dest_row, dest_col)
        if taking_piece.color == threatened_piece.color:
            return False
        else:
            return taking_piece.allowed_to_take(dest_row, dest_col)
    

class Piece(object):
    def __init__(self):
        pass

    def move_to(self, dest_row, dest_col):
        self.row = dest_row
        self.col = dest_col    

    def update_pos(self, x, y):
        """Sets the coordinates of the center of a piece to (x, y)."""
        self.image_rect.center = (x, y)

    def resting_pos(self):
        """Sets the coordinates of the center of a piece where it should be if it isn't moving."""
        self.image_rect.center = ((self.col+0.5)*self.tile_size, (self.row+0.5)*self.tile_size)

    def position(self, x = 0, y = 0):
        if self.moving:
            self.image_rect.center = (x, y)
        else:
            self.image_rect.center = ((self.col+0.5)*self.tile_size, (self.row+0.5)*self.tile_size)



    def draw(self, win):
        """Draws the piece on a window"""
        win.blit(self.image, self.image_rect)
    
    def is_not_empty(self):
        if self.color:
            return True


class Pawn(Piece):
    def __init__(self, row, col, color, width):
        self.row = row
        self.col = col
        self.image_path = os.path.join(os.getcwd(), "resources","w_p.png") if color == "w" else os.path.join(os.getcwd(), "resources","b_p.png")
        self.color = color
        self.image = pygame.image.load(self.image_path)
        self.width = width
        self.image = pygame.transform.scale(self.image, (width//8*0.9, width//8*0.9))
        self.image_rect = self.image.get_rect()
        self.tile_size = self.width // 8
        self.image_rect.center = ((self.col+0.5)*self.tile_size, (self.row+0.5)*self.tile_size)
        self.moving = False

    def allowed_moves(self):
        if self.color == "w":
            return [(-1, 0)]
        elif self.color == "b":
            return [(1, 0)]
    
    def allowed_to_move(self, dest_row, dest_col, white_to_move):
        if (self.color == "w" and white_to_move) or (self.color == "b" and not white_to_move):
            allowed_dests = [(self.row + move[0], self.col + move[1]) for move in self.allowed_moves()]
            if (dest_row, dest_col) in allowed_dests:
                return True

        return False
    
    def allowed_takes(self):
        if self.color == "w":
            return [(-1, 1), (-1, -1)]
        elif self.color == "b":
            return [(1, 1), (1, -1)]

    def allowed_to_take(self, dest_row, dest_col):
        allowed_takes =  [(self.row + move[0], self.col + move[1]) for move in self.allowed_takes()]
        if (dest_row, dest_col) in allowed_takes:
            return True
        return False

class Knight(Piece):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.image_path = os.path.join(os.getcwd(), "resources","w_n.png") if color == "w" else os.path.join(os.getcwd(), "resources","b_n.png")
        self.color = color
        self.image = pygame.image.load(self.image_path)


class Bishop(Piece):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.image_path = os.path.join(os.getcwd(), "resources","w_b.png") if color == "w" else os.path.join(os.getcwd(), "resources","b_b.png")
        self.color = color
        self.image = pygame.image.load(self.image_path)


class Rook(Piece):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.image_path = os.path.join(os.getcwd(), "resources","w_r.png") if color == "w" else os.path.join(os.getcwd(), "resources","b_r.png")
        self.color = color
        self.image = pygame.image.load(self.image_path)


class Queen(Piece):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.image_path = os.path.join(os.getcwd(), "resources","w_q.png") if color == "w" else os.path.join(os.getcwd(), "resources","b_q.png")
        self.color = color
        self.image = pygame.image.load(self.image_path)
    

class King(Piece):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.image_path = os.path.join(os.getcwd(), "resources","w_k.png") if color == "w" else os.path.join(os.getcwd(), "resources","b_k.png")
        self.color = color
        self.image = pygame.image.load(self.image_path)
