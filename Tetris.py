﻿

# -*- coding: utf-8 -*-
import copy
import random
import sys
import Tkinter

#===============================================================================
# global constant
#===============================================================================
BOARD_WIDTH = 12 #Hur stort fönstret ska vara
BOARD_HEIGHT = 24 

UNIT_X = 18 #Hur många pixlar varje "unit" är
UNIT_Y = 18 

PIECE_INIT_X = 3 #Kordinater för startpositionen, startar ovanför skärmen så att man inte ser biten direkt
PIECE_INIT_Y = -4 

DIFFICULTY = 1

BACKGROUND_COLOR = '#333'

#===============================================================================
# piece
#===============================================================================
    #Färg på alla bitarna
I_PIECE_EASY = 1
L_PIECE_EASY = 3
O_PIECE_EASY = 4

I_PIECE_NORMAL = 1
J_PIECE_NORMAL = 2
L_PIECE_NORMAL = 3
O_PIECE_NORMAL = 4
S_PIECE_NORMAL = 8
T_PIECE_NORMAL = 9
Z_PIECE_NORMAL = 10

I_PIECE_HARD = 1
J_PIECE_HARD = 2
L_PIECE_HARD = 3
O_PIECE_HARD = 4
X_PIECE_HARD = 5
H_PIECE_HARD = 6
Y_PIECE_HARD = 7

if DIFFICULTY == 0:

    ALL_PIECES = [ #Namn på alla bitar
        I_PIECE_EASY,
        L_PIECE_EASY,
        O_PIECE_EASY
    ]

if DIFFICULTY == 1:

    ALL_PIECES = [ #Namn på alla bitar
        I_PIECE_NORMAL,

        J_PIECE_NORMAL,

        L_PIECE_NORMAL,

        O_PIECE_NORMAL,

        S_PIECE_NORMAL,

        T_PIECE_NORMAL,

        Z_PIECE_NORMAL
    ]

if DIFFICULTY == 2:

    ALL_PIECES = [ #Namn på alla bitar
        I_PIECE_HARD,

        J_PIECE_HARD,

        L_PIECE_HARD,

        O_PIECE_HARD,

        X_PIECE_HARD,

        H_PIECE_HARD,

        Y_PIECE_HARD
    ]

PIECE_COLOR = { #Färg på alla bitar
    I_PIECE_EASY: "red",
    I_PIECE_NORMAL: "red",
    I_PIECE_HARD: "red",

    J_PIECE_NORMAL: "green",
    J_PIECE_HARD: "green",

    L_PIECE_EASY: "blue",
    L_PIECE_NORMAL: "blue",
    L_PIECE_HARD: "blue",

    O_PIECE_EASY: "yellow",
    O_PIECE_NORMAL: "yellow",
    O_PIECE_HARD: "yellow",

    X_PIECE_HARD: "orange",

    H_PIECE_HARD: "blue",

    Y_PIECE_HARD: "pink",

    S_PIECE_NORMAL: "purple",

    T_PIECE_NORMAL: "white",

    Z_PIECE_NORMAL: "brown"
}

"""
shape = lambda pc: [((z >> 2) + 1, z & 3) for z in range(16) if (pc >> z) & 1]
"""


if DIFFICULTY == 0:

    PIECE_SHAPE = {
        I_PIECE_EASY: [(1, 0), (1, 1)],
        L_PIECE_EASY: [(1, 0), (1, 1), (2, 1)],
        O_PIECE_EASY: [(1, 0), (1, 1), (2, 0), (2, 1)] #Skapar de olika bitarna genom kordinater
    }

elif DIFFICULTY == 1:
    PIECE_SHAPE = {
        I_PIECE_NORMAL: [(1, 0), (1, 1), (1, 2), (1, 3)],
        J_PIECE_NORMAL: [(1, 1), (1, 2), (1, 3), (2, 1)],
        L_PIECE_NORMAL: [(1, 0), (1, 1), (1, 2), (2, 2)],
        O_PIECE_NORMAL: [(1, 1), (1, 2), (2, 1), (2, 2)],
        S_PIECE_NORMAL: [(1, 1), (1, 2), (2, 2), (2, 3)],
        T_PIECE_NORMAL: [(1, 0), (1, 1), (1, 2), (2, 1)],
        Z_PIECE_NORMAL: [(1, 2), (1, 3), (2, 1), (2, 2)]
}

elif DIFFICULTY == 2:
    PIECE_SHAPE = {
        I_PIECE_HARD: [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
        J_PIECE_HARD: [(1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
        L_PIECE_HARD: [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)],
        O_PIECE_HARD: [(1, 0), (1, 1), (1, 2), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2)],
        X_PIECE_HARD: [(1, 0), (1, 2), (2, 1), (3, 0), (3, 2)],
        H_PIECE_HARD: [(1, 0), (1, 1), (1, 2), (2, 1), (3, 0), (3, 1), (3, 2)],
        Y_PIECE_HARD: [(1, 0), (2, 1), (2, 2), (3, 0)]
    }

def new_piece(): #Gör att nästa bit som skapas är en slumpmässigt vald av bitarna i "ALL_PIECES"
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
def move_piece_left(): #Flyttar biten till vänster om den inte blir blockerad
    global px
    npx = px - 1
    if not collide(piece, npx, py):
        px = npx 


def move_piece_right(): #Flyttar biten till höger om den inte blir blockerad
    global px
    npx = px + 1
    if not collide(piece, npx, py):
        px = npx 


def rotate_piece(): #Roterar biten om den kan roteras utan att krocka i något runtom den
    global piece
    npiece = [(j, 3 - i) for (i, j) in piece]
    if not collide(npiece, px, py):
        piece = npiece 


def fall_piece(): #Gör att biten faller nedåt 1 ruta i taget tills den antingen landar på en bit eller på botten av spel-planen
    global py
    for j in range(py, BOARD_HEIGHT):
        py = j
        if collide(piece, px, j + 1):
            return 


#===============================================================================
# drawing transform
#===============================================================================
def map_to_ui_x(i): #Uppdaterar det visuella, att biten åker höger/vänster
    return i * UNIT_X 


def map_to_ui_y(j): #Uppdaterar när biten flyttas nedåt
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
    score = 0 #Startar om scoren från 0 när spelet börjar


def get_score():
    return score #Hämtar scoren som sedan anropas för att visa den vid "game over"


def incr_score(value):
    global score
    assert isinstance(value, int), value
    score += value #Ökar scoren varje gång en line clearas


#===============================================================================
# collide
#===============================================================================
"""
collide = lambda piece, px, py: [1 for (i, j) in piece if board[j + py][i + px]] #是否碰撞
"""
def collide(piece, px, py): #Gör att biten stannar när den landar på en annan bit eller når botten av planen
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


def place_piece(piece, px, py, pc): #Tillåter dig att flytta biten åt höger/vänster/nedåt så länge den inte blockeras av en annan bit eller planens kant/botten
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


def clear_complete_lines(): #Tar bort en line när den blir helt fylld
    global board
    nb = [l for l in board if 0 in l] # 
    s = len(board) - len(nb)
    if s:
        board = new_board_lines(s) + nb
    return s


#===============================================================================
# 
#===============================================================================
def game_over(): #Säger gameover och hämtar scoren
    sys.exit("GAME OVER: score %i" % get_score()) 


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
        fall_piece() #Anropar funktionerna när piltangenterna används

    if e == None:
        if collide(piece, px, py + 1):
            if py < 0:
                game_over()
                return  #Ger gameover och anropar game_over funktionen när bitarna kommer för högt upp så att spelet inte kan fortsättas

            place_piece(piece, px, py, pc)

            piece, pc = new_piece()
            px, py = PIECE_INIT_X, PIECE_INIT_Y

        else:
            py += 1

        s = clear_complete_lines()
        if s:
            incr_score(2 ** s) 

        scr.after(300, tick)

    redraw_ui() #Uppdaterar UI hela tiden


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

def init_tetris(): #Anropar alla funktioner som behövs för att börja spela, spelplan, bitarna som kommer användas och att scoren startar på 0
    global board, piece, pc, scr
    board = new_board_lines(BOARD_HEIGHT)
    piece, pc = new_piece() 
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

