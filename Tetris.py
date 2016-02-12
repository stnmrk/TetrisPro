# -*- coding: utf-8 -*-
import copy
import random
import sys
import Tkinter

#===============================================================================
# global constant
#===============================================================================
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

UNIT_X = 30
UNIT_Y = 30

PIECE_INIT_X = 3
PIECE_INIT_Y = -2

BACKGROUND_COLOR = '#000'

#===============================================================================
# piece
#===============================================================================
I_PIECE = 0xf
J_PIECE = 0x2e
L_PIECE = 0x47
O_PIECE = 0x66
S_PIECE = 0xC6
T_PIECE = 0x27
Z_PIECE = 0x6C

ALL_PIECES = [
    I_PIECE,
    J_PIECE,
    L_PIECE,
    O_PIECE,
    S_PIECE,
    T_PIECE,
    Z_PIECE
]

PIECE_COLOR = {
    I_PIECE: "red",
    J_PIECE: "#0f0",
    L_PIECE: "#ff0",
    O_PIECE: "#0ff",
    S_PIECE: "#38f",
    T_PIECE: "blue",
    Z_PIECE: "#f0f"
}

"""
shape = lambda pc: [((z >> 2) + 1, z & 3) for z in range(16) if (pc >> z) & 1]
"""
PIECE_SHAPE = {
    I_PIECE: [(1, 0), (1, 1), (1, 2), (1, 3)],
    J_PIECE: [(1, 1), (1, 2), (1, 3), (2, 1)],
    L_PIECE: [(1, 0), (1, 1), (1, 2), (2, 2)],
    O_PIECE: [(1, 1), (1, 2), (2, 1), (2, 2)],
    S_PIECE: [(1, 1), (1, 2), (2, 2), (2, 3)],
    T_PIECE: [(1, 0), (1, 1), (1, 2), (2, 1)],
    Z_PIECE: [(1, 2), (1, 3), (2, 1), (2, 2)]
}

def new_piece():
    p = random.choice(ALL_PIECES)
    p_shape = copy.deepcopy(PIECE_SHAPE[p])
    return p_shape, p


#===============================================================================
# piece : action
#===============================================================================
"""
    npx = px + (-1 if keys == "Left" else (1 if keys == "Right" else 0)) # 左-1右1否則0
    npiece = [(j, 3 - i) for (i, j) in piece] if keys == "Up" else piece   #rotate
    if not collide(npiece, npx, py):
        piece, px = npiece, npx
    if keys == "Down":
        py = (j for j in range(py, BOARD_HEIGHT) if collide(piece, px, j + 1)).next()
"""
def move_piece_left():
    global px
    npx = px - 1
    if not collide(piece, npx, py):
        px = npx


def move_piece_right():
    global px
    npx = px + 1
    if not collide(piece, npx, py):
        px = npx


def rotate_piece():
    global piece
    npiece = [(j, 3 - i) for (i, j) in piece]
    if not collide(npiece, px, py):
        piece = npiece


def fall_piece():
    global py
    for j in range(py, BOARD_HEIGHT):
        py = j
        if collide(piece, px, j + 1):
            return


#===============================================================================
# drawing transform
#===============================================================================
def map_to_ui_x(i):
    return i * UNIT_X


def map_to_ui_y(j):
    return j * UNIT_Y


def ui_create_rect(i, j, color):
    assert isinstance(i, int), i
    assert isinstance(j, int), j
    x0 = map_to_ui_x(i)
    y0 = map_to_ui_y(j)
    x1 = map_to_ui_x(i + 1)
    y1 = map_to_ui_y(j + 1)
    scr.create_rectangle(x0, y0, x1, y1, fill=color)


def redraw_ui():
    piece_region = [(i + px, j + py) for i, j in piece]

    scr.delete("all")
    for i, j in [(i, j) for i in range(BOARD_WIDTH) for j in range(BOARD_HEIGHT)]:
        if (i, j) in piece_region:
            color = PIECE_COLOR[pc]
        else:
            color = PIECE_COLOR.get(board[j][i], BACKGROUND_COLOR)
        ui_create_rect(i, j, color)


#===============================================================================
# score
#===============================================================================
def reset_score():
    global score
    score = 0


def get_score():
    return score


def incr_score(value):
    global score
    assert isinstance(value, int), value
    score += value


#===============================================================================
# collide
#===============================================================================
"""
collide = lambda piece, px, py: [1 for (i, j) in piece if board[j + py][i + px]] #是否碰撞
"""
def collide(piece, px, py):
    assert isinstance(px, int), px
    assert isinstance(py, int), py
    for (i, j) in piece:
        x = px + i
        y = py + j
        if not (0 <= x < BOARD_WIDTH):
            return True
        if y >= BOARD_HEIGHT:
            return True
        if y < 0:
            continue
        if board[y][x]:
            return True
    return False


#===============================================================================
# board
#===============================================================================
def new_board_lines(num):
    assert isinstance(num, int), num
    return [[0] * BOARD_WIDTH for j in range(num)]


board = new_board_lines(BOARD_HEIGHT)


def place_piece(piece, px, py, pc):
    """
    for i, j in piece:
        board[j + py][i + px] = pc
    """
    for i, j in piece:
        x = px + i
        y = py + j
        if not (0 <= x < BOARD_WIDTH):
            continue
        if not (0 <= y < BOARD_HEIGHT):
            continue
        board[y][x] = pc


def clear_complete_lines():
    global board
    nb = [l for l in board if 0 in l] # 沒有被填滿的
    s = len(board) - len(nb)
    if s:
        board = new_board_lines(s) + nb
    return s


#===============================================================================
# 
#===============================================================================
def game_over():
    sys.exit("GAME OVER: score %i" % get_score()) # game over 的狀況


#===============================================================================
# tick
#===============================================================================
def tick(e=None):
    global piece, px, py, pc

    keys = e.keysym if e else  "" # get key event

    if keys == 'Left':
        move_piece_left()
    elif keys == 'Right':
        move_piece_right()
    elif keys == 'Up':
        rotate_piece()
    elif keys == 'Down':
        fall_piece()

    if e == None:
        if collide(piece, px, py + 1):
            if py < 0:
                game_over()
                return

            place_piece(piece, px, py, pc)

            piece, pc = new_piece()
            px, py = PIECE_INIT_X, PIECE_INIT_Y

        else:
            py += 1

        s = clear_complete_lines()
        if s:
            incr_score(2 ** s)

        scr.after(300, tick)

    redraw_ui()


#===============================================================================
# initial
#===============================================================================
board = None
piece = None
pc = None
px = PIECE_INIT_X
py = PIECE_INIT_Y
score = 0
scr = None

def init_tetris():
    global board, piece, pc, scr
    board = new_board_lines(BOARD_HEIGHT)
    piece, pc = new_piece() # 第一個piece
    reset_score()

    scr = Tkinter.Canvas(width=map_to_ui_x(BOARD_WIDTH), height=map_to_ui_y(BOARD_HEIGHT), bg=BACKGROUND_COLOR)
    scr.after(300, tick)
    scr.bind_all("<Key>", tick)
    scr.pack()
    scr.mainloop()

#  for line in board: print '\t'.join(str(v) for v in line)
#  print len(board)
#  print px,py

if __name__ == '__main__':
    init_tetris()
