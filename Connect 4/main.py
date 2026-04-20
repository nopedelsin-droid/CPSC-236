# Mike Benko IV
# CSPC236 - Final Project
# main.py

import pygame
import sys            # imports fonts for game
import numpy as np
import ai             # computer opponent file

pygame.init()
pygame.mixer.init()

# Inizlizing game sounds
drop_sound = pygame.mixer.Sound('drop.wav')
win_sound = pygame.mixer.Sound('cheer.wav')
lose_sound = pygame.mixer.Sound('horn.wav')

# global constants for board and window
ROW_COUNT = 6
COL_COUNT = 7
SQUARESIZE = 100
WIDTH = COL_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE  # 700 pixels
RADIUS = int(SQUARESIZE / 2 - 5)

# global constants for colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# define screen and font for game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("monospace", 75)

# function to generate board
def create_board():
    return np.zeros((ROW_COUNT, COL_COUNT))                 # uses numpy to generate coordinate system starting at all zeros

# function handling piece drop coordinates transfer
def drop_piece(board, row, col, piece):
    board[row][col] = piece                                 # pass board coordinates of the played piece
    drop_sound.play()  # plays drop sound

# function checking for legal moves
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0                   # pass coordinates of all empty row/column combinations

# function to determine empty row/col combination
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# function to check for all possible winning conditions
def winning_move(board, piece):
    # Standard 4-in-a-row check
    for c in range(COL_COUNT - 3):                                                      # for-loop check for horizontal game win condition
        for r in range(ROW_COUNT):                                                        # iterate x coordinate check static y coordinate check
            if all(board[r][c + i] == piece for i in range(4)): return True                 # iterate through x pos coordinates - pass true for all same piece
    for c in range(COL_COUNT):                                                          # for-loop check for vertical game win condition
        for r in range(ROW_COUNT - 3):                                                    # static x coordinate check iterate y coordinate check
            if all(board[r + i][c] == piece for i in range(4)): return True                 # iterate through y pos coordinates - pass true for all same pieces
    for c in range(COL_COUNT - 3):                                                      # for-loop check for positive diagonal game win condition
        for r in range(ROW_COUNT - 3):                                                    # x coordinate check inverted y coordinate check
            if all(board[r + i][c + i] == piece for i in range(4)): return True             # iterate both x, y pos coordinates - pass true for all same pieces
    for c in range(COL_COUNT - 3):                                                      # for-loop check for negative diagonal game win condition
        for r in range(3, ROW_COUNT):                                                     # inverted x coordinate check normal y coordinate check
            if all(board[r - i][c + i] == piece for i in range(4)): return True             # iterate both x-i, y+i pos coordinates - pass true for all same pieces
    return False

# function handling pygame draw definitions for gameboard
def draw_board(board):
    # clear the board area (below the top bar - piece playing area)
    pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, WIDTH, HEIGHT - SQUARESIZE))                                   # NOTE: the height-squaresize allows a buffer above playfield

    # first nested for loop generates background and the grid playfield
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))  # NOTE: blue draw covers entire playfield horizontally but leaves buffer
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                               int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)              # NOTE: black draw subtracts circular portion of blue for each play coordinate

    # second nested for loop generates both players respective pieces when called
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != 0:                                                                                        # When column/row combo has a piece played, the value for the cell is 1
                color = RED if board[r][c] == 1 else YELLOW                                                               # depending on turn of play, piece is either yellow or red
                y_pos = int(HEIGHT - (r * SQUARESIZE + SQUARESIZE / 2))                                                     # determine cell coordinates of played piece
                pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), y_pos), RADIUS)               # draw respective piece and color and apply to gameboard

    # force update to display gameboard
    pygame.display.update()

# main game running function handling inputs and updates
def run_game(vs_ai=False):
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))                                            # apply new window size (Menu window is not a direct match)

    board = create_board()                                                                       # call create board function to generate
    game_over = False                                                                            # initialize game state boolean
    turn = 0                                                                                     # initialize turn index at 0
    draw_board(board)                                                                            # finally draw gameboard using function call

    while not game_over:                                                                         # encapsulating while loop using game state boolean
        for event in pygame.event.get():                                                           # for loop to execute for all pygame even handlers
            if event.type == pygame.QUIT:                                                            # if statement for safely closing game components
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:                                                     # if-loop handling mouse position for drawing game pieces
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                elif not vs_ai and turn == 1:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:                                             # nested if-loop handling mouse click events
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)                                                      # attempts to determine selected col based on closest position

                if turn == 0 and is_valid_location(board, col):                                    # second nest if does play validate for player 1 (red) moves
                    row = get_next_open_row(board, col)                                              # check selected row for state to determine drop placement
                    drop_piece(board, row, col, 1)                                             # call piece coordinate function to store play data

                    draw_board(board)                                                                # force update played piece to gameboard

                    if winning_move(board, 1):                                                 # check win possible win condition for player 1 (red)
                        win_sound.play()  # Pays win sound for player 1
                        label = font.render("Player 1 wins!!", 1, RED)                    # display winner in upper play field
                        screen.blit(label, (40, 10))
                        pygame.display.update()                                                        # force push updates to the display
                        game_over = True                                                               # update loop boolean condition
                    turn = 1                                                                         # if not a winning move, set turn counter to 1

                elif not vs_ai and turn == 1 and is_valid_location(board, col):                    # nested elif to validate HUMAN player 2 moves (yellow)
                    row = get_next_open_row(board, col)                                              # validate for open rows in playfield
                    drop_piece(board, row, col, 2)                                             # apply piece drop to selected row/column with turn counter 2
                    draw_board(board)                                                                # force update board with newly played piece

                    if winning_move(board, 2):                                                 # if statement to check if played piece is winning move
                        label = font.render("Player 2 wins!!", 1, YELLOW)                 # if a winning move, print win on top of playfield
                        win_sound.play()  # Pays win sound for player 2
                        screen.blit(label, (40, 10))
                        pygame.display.update()                                                        # force update changes to playfield
                        game_over = True                                                               # update game state boolean to end the game
                    turn = 0                                                                         # if not a winning move, reset turn counter to 0

        # AI TURN (Moved outside human event loop)
        if vs_ai and turn == 1 and not game_over:                                 # nested if for only AI player 2 (yellow) moves
            pygame.time.wait(500)                                                   # add small delay to computer moves - simulate "thinking"
            col = ai.pick_best_move(board, 2)                                 # call ai.py function for computer play determination
            if is_valid_location(board, col):                                       # if statement to pass valid locations from ai.py
                row = get_next_open_row(board, col)                                   # open row check for computer plays
                drop_piece(board, row, col, 2)                                  # apply play to board using function call
                draw_board(board)                                                     # force update board

                if winning_move(board, 2):                                      # if statement to check for winning play by the ai
                    lose_sound.play()  # Plays lose sound
                    label = font.render("AI wins!!", 1, YELLOW)            # winning move prints winner in upper buffer
                    screen.blit(label, (40, 10))
                    pygame.display.update()                                             # force update board with label
                    game_over = True                                                    # update game state boolean

                turn = 0                                                              # non-winning move resets turn counter to 0
                # Wipe out any clicks made while AI was "thinking"
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)                            # NOTE: this section was added to avoid 'dead clicks' by the human player

    # wait timer before returning to menu screen
    pygame.time.wait(3000)