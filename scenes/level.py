import pygame
import random
from utils import *

unit = 24

das = 7
arr = 1
sdf = 0.5
board_over = 4

skin_img = pygame.image.load("data/skin.png").convert()

imgs = {
    "I": pygame.Surface((unit, unit)),
    "J": pygame.Surface((unit, unit)),
    "L": pygame.Surface((unit, unit)),
    "O": pygame.Surface((unit, unit)),
    "S": pygame.Surface((unit, unit)),
    "T": pygame.Surface((unit, unit)),
    "Z": pygame.Surface((unit, unit)),
    "B": pygame.Surface((unit, unit))
}

for i, img in enumerate(imgs):
    imgs[img].blit(skin_img, (-unit*i, 0))

I = [
    [0, 0, 0, 0],
    ["I", "I", "I", "I"],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

J = [
    ["J", 0, 0],
    ["J", "J", "J"],
    [0, 0, 0]
]

L = [
    [0, 0, "L"],
    ["L", "L", "L"],
    [0, 0, 0]
]

O = [
    [0, "O", "O", 0],
    [0, "O", "O", 0]
]

S = [
    [0, "S", "S"],
    ["S", "S", 0],
    [0, 0, 0]
]

T = [
    [0, "T", 0],
    ["T", "T", "T"],
    [0, 0, 0]
]

Z = [
    ["Z", "Z", 0],
    [0, "Z", "Z"],
    [0, 0, 0]
]

ids = {
    str(I): "I",
    str(J): "J",
    str(L): "L",
    str(O): "O",
    str(S): "S",
    str(T): "T",
    str(Z): "Z"
}

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
            if dot != 0:
                dot_x = x+dx
                dot_y = y+dy
                if dot_x < 0 or dot_x >= 10 or dot_y >= 20:
                    return False
                elif dot_y > 0:
                    if board[dot_y+board_over][dot_x] != 0:
                        return False
    return True

def rotateable(mino_t, mino, dx, dy, board, r, dr):
    key = f"{r}{(r+dr)%4}"
    rotated_mino = rotate(mino, dr)
    offset_data = I_OFFSETS[key]
    if mino_t in JLTSZ_BLOCKS:
        offset_data = JLTSZ_OFFSETS[key]
    elif mino_t == O:
        offset_data = [[0, 0]]
    for offset in offset_data:
        if moveable(rotated_mino, dx+offset[0], dy-offset[1], board):
            return dx+offset[0], dy-offset[1]

def rotate(mino, dr):
    if dr == 1:
        return list(zip(*mino[::-1]))
    elif dr == -1:
        return list(zip(*mino))[::-1]
    else:
        return rotate(rotate(mino, 1), 1)

def lock(mino_t, mino, dx, dy, board):
    for y, row in enumerate(mino):
        for x, dot in enumerate(row):
            if dot != 0:
                board[y+dy+board_over][x+dx] = ids[str(mino_t)]

def line_clear(board):
    for row in board:
        clear = True
        for dot in row:
            if dot == 0:
                clear = False
        if clear:
            board.remove(row)
            board.insert(0, [0 for i in range(10)])

class Level:
    def __init__(self, screen, gm):
        self.screen: pygame.Surface = screen
        self.gm = gm
        self.cx = screen_width/2-unit*5 
        self.cy = screen_height/2-unit*10

        next_minos = ALL_BLOCKS[:]
        random.shuffle(next_minos)
        self.next = [*next_minos]

        self.mino_t = self.next.pop(0)
        self.mino = self.mino_t[:]
        self.mino_x = 3
        self.mino_y_t = 0
        self.mino_y = -board_over
        self.mino_r = 0

        self.das_t = 0
        self.arr_t = 0
        self.sdf_t = 0

        self.lock_t = 0

        self.dir = 0
        self.r_dir = 0

        self.board = [[0 for _ in range(10)] for _ in range(20+board_over)]

        self.hold = None
        self.holdable = True

        self.shadow_mino = self.mino[:]
        self.shadow_mino_y = self.mino_y
        self.mino_ox = 0
        self.mino_oy = 0
        self.mino_or = 0

    def set(self, mino=None):
        if mino == None:
            self.mino_t = self.next.pop(0)
        else:
            self.mino_t = mino
        self.mino = self.mino_t[:]
        if len(self.next) <= 5:
            next_minos = ALL_BLOCKS[:]
            random.shuffle(next_minos)
            self.next += next_minos

        self.mino_x = 3
        self.mino_y_t = 0
        self.mino_y = -3
        self.mino_r = 0

        self.holdable = True

        line_clear(self.board)
        self.reset_shadow()

    def reset_shadow(self):
        self.mino_ox = self.mino_x
        self.mino_oy = self.mino_y
        self.mino_or = self.mino_r

        self.shadow_mino = self.mino[:]
        self.shadow_mino_y = self.mino_y
        for i in range(1, 20+board_over):
            if moveable(self.shadow_mino, self.mino_x, self.shadow_mino_y+1, self.board):
                self.shadow_mino_y += 1
            else:
                break

    def run(self, dt, events):
        self.screen.fill("#3A3A3A")

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.dir = 1
                if event.key == pygame.K_LEFT:
                    self.dir = -1
                if event.key == pygame.K_UP:
                    self.r_dir = 1
                if event.key == pygame.K_LCTRL:
                    self.r_dir = -1
                if event.key == pygame.K_a:
                    self.r_dir = 0
                if event.key == pygame.K_SPACE:
                    for i in range(1, 20+board_over):
                        if moveable(self.mino, self.mino_x, self.mino_y+1, self.board):
                            self.mino_y += 1
                        else:
                            break
                    lock(self.mino_t, self.mino, self.mino_x, self.mino_y, self.board)
                    self.lock_t = 0
                    self.set()
                if event.key == pygame.K_LSHIFT and self.holdable:
                    if self.hold == None:
                        self.hold = self.mino_t[:]
                        self.set()
                    else:
                        hold_mino = self.mino_t[:]
                        self.set(self.hold)
                        self.hold = hold_mino[:]
                    self.holdable = False

                if self.r_dir != 99:
                    rotated = rotateable(self.mino_t, self.mino, self.mino_x, self.mino_y, self.board, self.mino_r, self.r_dir)
                    if rotated:
                        self.mino_r = (self.mino_r+self.r_dir)%4
                        self.mino_x, self.mino_y = rotated
                        self.mino = rotate(self.mino, self.r_dir)
                        self.lock_t = 0
                    self.r_dir = 99
                    self.reset_shadow()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    if moveable(self.mino, self.mino_x+self.dir, self.mino_y, self.board):
                        self.mino_x += self.dir
                    self.das_t = 0
                    self.arr_t = 0
                    self.lock_t = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.dir = 1
            else:
                self.dir = -1
            if self.das_t < das:
                self.das_t += dt
            else:
                if arr == 0:
                    for i in range(0, 10):
                        if moveable(self.mino, self.mino_x+self.dir, self.mino_y, self.board):
                            self.mino_x += self.dir
                        else:
                            break
                else:
                    self.arr_t += dt
                    for i in range(int(arr)*2):
                        if self.arr_t >= arr:
                            self.arr_t -= arr
                            if self.arr_t < 0:
                                break
                            if moveable(self.mino, self.mino_x+self.dir, self.mino_y, self.board):
                                self.mino_x += self.dir
                            
        if keys[pygame.K_DOWN]:
            if sdf == 0:
                for i in range(1, 20+board_over):
                    if moveable(self.mino, self.mino_x, self.mino_y+1, self.board):
                        self.mino_y += 1
                    else:
                        break
            else:
                self.sdf_t += dt
                for i in range(int(sdf)*2):
                    if self.sdf_t > sdf:
                        self.sdf_t -= sdf
                        if self.sdf_t < 0:
                            break
                        if moveable(self.mino, self.mino_x, self.mino_y+1, self.board):
                            self.mino_y += 1

        self.mino_y_t += dt/64
        if self.mino_y_t >= 1:
            self.mino_y_t = 0
            if moveable(self.mino, self.mino_x, self.mino_y+1, self.board):
                self.mino_y += 1
    
        if not moveable(self.mino, self.mino_x, self.mino_y+1, self.board):
            self.lock_t += dt
            if self.lock_t >= 30:
                lock(self.mino_t, self.mino, self.mino_x, self.mino_y, self.board)
                self.lock_t = 0
                self.set()

        if self.mino_x != self.mino_ox or self.mino_y != self.mino_oy or self.mino_r != self.mino_or:
            self.reset_shadow()

        for i in range(0, 20+1):
            pygame.draw.line(self.screen, "#4f4f4f", (self.cx, self.cy+i*unit), (self.cx+10*unit, self.cy+i*unit), 2)
        for i in range(0, 10+1):
            pygame.draw.line(self.screen, "#4f4f4f", (self.cx+i*unit, self.cy), (self.cx+i*unit, self.cy+20*unit), 2)
                
        for y, row in enumerate(self.shadow_mino):
            for x, dot in enumerate(row):
                if dot != 0:
                    self.screen.blit(imgs["B"], (self.cx+(self.mino_x+x)*unit, self.cy+(self.shadow_mino_y+y)*unit))

        for y, row in enumerate(self.mino):
            for x, dot in enumerate(row):
                if dot != 0:
                    self.screen.blit(imgs[ids[str(self.mino_t)]], (self.cx+(self.mino_x+x)*unit, self.cy+(self.mino_y+y)*unit))
        
        if self.hold != None:
            offset_x = 0.5
            offset_y = 0
            if self.hold == I:
                offset_x = 0
                offset_y = -0.5
            for y, row in enumerate(self.hold):
                for x, dot in enumerate(row):
                    if dot != 0:
                        self.screen.blit(imgs[ids[str(self.hold)]], ((self.cx+(x-5+offset_x)*unit, self.cy+(y+offset_y)*unit)))

        for i, mino in enumerate(self.next[:5]):
            offset_x = 0.5
            offset_y = 0
            if mino == I:
                offset_x = 0
                offset_y = -0.5
            for y, row in enumerate(mino):
                for x, dot in enumerate(row):
                    if dot != 0:
                        self.screen.blit(imgs[ids[str(mino)]], ((self.cx+(11+x+offset_x)*unit, self.cy+(i*3+y+offset_y)*unit)))
                    
        for y, row in enumerate(self.board):
            for x, dot in enumerate(row):
                if dot != 0:
                    self.screen.blit(imgs[dot], ((self.cx+x*unit, self.cy+(y-board_over)*unit)))