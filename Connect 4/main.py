import pygame
import sys            # imports fonts for game
import numpy as np
import ai             # computer opponent file

pygame.init()
pygame.mixer.init()

# global constants for board and window
ROW_COUNT = 6
COL_COUNT = 7
SQUARESIZE = 100
WIDTH = COL_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE  # 700 pixels
RADIUS = int(SQUARESIZE / 2 - 5)

# Inizlizing game sounds
drop_sound = pygame.mixer.Sound('drop.wav')
win_sound = pygame.mixer.Sound('cheer.wav')
lose_sound = pygame.mixer.Sound('horn.wav')

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
    return np.zeros((ROW_COUNT, COL_COUNT))

# function handling piece drop coordinates passing
def drop_piece(board, row, col, piece):
    board[row][col] = piece
    drop_sound.play()           #plays drop sound

# function checking for legal moves
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

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
    # Clear the board area (below the top bar - piece playing area)
    pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, WIDTH, HEIGHT - SQUARESIZE))

    # first nested for loop generates background and the grid playfield
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                               int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # second nested for loop generates both players respective pieces when called
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != 0:
                color = RED if board[r][c] == 1 else YELLOW
                y_pos = int(HEIGHT - (r * SQUARESIZE + SQUARESIZE / 2))
                pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), y_pos), RADIUS)

    # force update to display gameboard
    pygame.display.update()

# main game running function handling inputs and updates
def run_game(vs_ai=False):
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    board = create_board()
    game_over = False
    turn = 0
    draw_board(board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                              # if statement for safely closing game components
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:                                                       # if-loop handling mouse position for drawing game pieces
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                elif not vs_ai and turn == 1:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:                                                   # nested if-loop handling mouse click events
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)                                                            # attempts to determine selected col based on closest position

                if turn == 0 and is_valid_location(board, col):                                          # second nest if does play validate for player 1 (red) moves
                    row = get_next_open_row(board, col)                                                    # check selected row for state to determine drop placement
                    drop_piece(board, row, col, 1)                                                   # call piece coordinate function to store play data

                    draw_board(board)                                                                      # force update played piece to gameboard

                    if winning_move(board, 1):                                                       # check win possible win condition for player 1 (red)
                        win_sound.play()     #Pays win sound for player 1
                        label = font.render("Player 1 wins!!", 1, RED)                          # display winner in upper play field
                        screen.blit(label, (40, 10))
                        pygame.display.update()                                                              # force push updates to the display
                        game_over = True                                                                     # update loop boolean condition
                    turn = 1

                elif not vs_ai and turn == 1 and is_valid_location(board, col):                          # nested elif to validate HUMAN player 2 moves (yellow)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    draw_board(board)

                    if winning_move(board, 2):
                        label = font.render("Player 2 wins!!", 1, YELLOW)
                        win_sound.play()  # Pays win sound for player 2
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                    turn = 0

        # AI TURN (Moved outside human event loop)
        if vs_ai and turn == 1 and not game_over:                                 # nested if for only AI player 2 (yellow) moves
            pygame.time.wait(500)                                                   # add small delay to computer moves - simulate "thinking"
            col = ai.pick_best_move(board, 2)                                 # call ai.py function for computer play determination
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                draw_board(board)

                if winning_move(board, 2):
                    lose_sound.play()        #Plays lose sound
                    label = font.render("AI wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    game_over = True

                turn = 0
                # Wipe out any clicks made while AI was "thinking"
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)

    # wait timer before returning to menu screen
    pygame.time.wait(3000)
