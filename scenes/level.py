import pygame
from utils import *

unit = 24

I = [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

J = [
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
]

L = [
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0]
]

O = [
    [0, 1, 1, 0],
    [0, 1, 1, 0]
]

S = [
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0]
]

T = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0]
]

Z = [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0]
]

JLTSZ_BLOCKS = [J, L, T, S, Z]
ALL_BLOCKS = [I, J, L, O, S, T, Z]

I_OFFSETS = {
    "01": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "10": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "12": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "21": [(0, 0), (1, 0) ,(-2, 0), (1, -2), (-2, 1)],
    "23": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "32": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "30": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "03": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "00": [(0, 0)],
    "11": [(0, 0)],
    "22": [(0, 0)],
    "33": [(0, 0)]
}

JLTSZ_OFFSETS = {
    "01": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "10": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "12": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "21": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "23": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "32": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "30": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "03": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "00": [(0, 0)],
    "11": [(0, 0)],
    "22": [(0, 0)],
    "33": [(0, 0)]
}

def moveable(mino, dx, dy, board):
    for y, row in enumerate(mino):
        for x, dot in enumerate(row):
            if dot == 1:
                dot_x = x+dx
                dot_y = y+dy
                if dot_x < 0 or dot_x >= 10 or dot_y < -3 or dot_y >= 20:
                    return
                if board[dot_y][dot_x] == 1:
                    return
    return True

def rotateable(mino_t, mino, dx, dy, board, r, dr):
    key = f"{r}{(r+dr)%4}"
    rotated_mino = rotate(mino, dr)
    offset_data = I_OFFSETS
    if mino_t in JLTSZ_BLOCKS:
        offset_data = JLTSZ_OFFSETS
    elif mino_t == O:
        offset_data = {[[0, 0]]}
    for offset in offset_data[key]:
        if moveable(rotated_mino, dx+offset[0], dy-offset[1], board):
            return dx+offset[0], dy-offset[1], rotated_mino

def rotate(mino, dr):
    if dr == 1:
        return list(zip(*mino[::-1]))
    elif dr == -1:
        return list(zip(*mino))[::-1]
    else:
        return rotate(rotate(mino, 1), 1)


class Level:
    def __init__(self, screen, gm):
        self.screen = screen
        self.gm = gm
        self.cx = screen_width/2-unit*5 
        self.cy = screen_height/2-unit*10

        self.mino_t = T
        self.mino = self.mino_t
        self.mino_x = 3
        self.mino_ay = -3
        self.mino_y = int(self.mino_ay)
        self.mino_r = 0

        self.board = [[0 for _ in range(10)] for _ in range(20)]

    def run(self, dt, events):
        self.screen.fill("#eeeeee")

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if moveable(self.mino, self.mino_x+1, self.mino_y, self.board):
                        self.mino_x += 1
                elif event.key == pygame.K_LEFT:
                    if moveable(self.mino, self.mino_x-1, self.mino_y, self.board):
                        self.mino_x -= 1
                elif event.key == pygame.K_UP:
                    rotated = rotateable(self.mino_t, self.mino, self.mino_x, self.mino_y, self.board, self.mino_r, 1)
                    if rotated != False:
                        self.mino_r = (self.mino_r+1)%4
                        self.mino_x, self.mino_y, self.mino = rotated
                    
        self.mino_ay += dt/64
        self.mino_y = int(self.mino_ay)

        for y, row in enumerate(self.mino):
            for x, dot in enumerate(row):
                if dot == 1:
                    pygame.draw.rect(self.screen, "#000000", (self.cx+(self.mino_x+x)*unit, self.cy+(self.mino_y+y)*unit, unit, unit))

        for i in range(0, 20+1):
            pygame.draw.line(self.screen, "#000000", (self.cx, self.cy+i*unit), (self.cx+10*unit, self.cy+i*unit))
        for i in range(0, 10+1):
            pygame.draw.line(self.screen, "#000000", (self.cx+i*unit, self.cy), (self.cx+i*unit, self.cy+20*unit))