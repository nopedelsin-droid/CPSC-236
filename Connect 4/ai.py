# Mike Benko IV
# CPSC236 - Final Project
# ai.py

import random  # random is used for ai plays when win or block condition cannot be met

# set playfield definitiona
ROW_COUNT = 6
COL_COUNT = 7

# function to validate open columns in playfield
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# function to request all currently available columns to play
def get_valid_locations(board):
    return [col for col in range(COL_COUNT) if is_valid_location(board, col)]   # NOTE: only returns a playable coordinate after validation check

# function to search for available rows to play in playfield
# noinspection PyInconsistentReturns
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):                     # for-loop to iterate through all rows on playfield
        if board[r][col] == 0:                       # if the row/column combo has no pieces return the row
            return r                                   # return coordinates of opening in row

# imported win condition definitions from main.py for ai to use separately
def winning_move(board, piece):
    for c in range(COL_COUNT-3):                                                   # for-loop check for horizontal game win condition
        for r in range(ROW_COUNT):                                                   # iterate x coordinate check static y coordinate check
            if all(board[r][c+i] == piece for i in range(4)): return True              # iterate through x pos coordinates - pass true for all same piece
    for c in range(COL_COUNT):                                                     # for-loop check for vertical game win condition
        for r in range(ROW_COUNT-3):                                                 # static x coordinate check iterate y coordinate check
            if all(board[r+i][c] == piece for i in range(4)): return True              # iterate through y pos coordinates - pass true for all same pieces
    for c in range(COL_COUNT-3):                                                   # for-loop check for positive diagonal game win condition
        for r in range(ROW_COUNT-3):                                                 # x coordinate check inverted y coordinate check
            if all(board[r+i][c+i] == piece for i in range(4)): return True            # iterate both x, y pos coordinates - pass true for all same pieces
    for c in range(COL_COUNT-3):                                                   # for-loop check for negative diagonal game win condition
        for r in range(3, ROW_COUNT):                                                # inverted x coordinate check normal y coordinate check
            if all(board[r-i][c+i] == piece for i in range(4)): return True            # iterate both x-i, y+i pos coordinates - pass true for all same pieces
    return False

# extremely basic 'ai' function to determine computer's play
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)   # request valid plays from main function
    opponent = 1 if piece == 2 else 2                # NOTE: ai is supposed to be 'player 2' but this statement will fix all edge cases

    # 1. Check for immediate win
    for col in valid_locations:                    # request all valid columns to play a piece (win condition)
        row = get_next_open_row(board, col)          # apply open row position to winning row play
        temp_board = board.copy()                    # pass copy of playfield to computer
        temp_board[row][col] = piece                 # find winning play for ai and place piece to win
        if winning_move(temp_board, piece):          # if play wins the game for ai, return the winning play
            return col

    # 2. Check for immediate block
    for col in valid_locations:                    # request all valid columns to play a piece (block condition)
        row = get_next_open_row(board, col)          # apply open row position to blocking row play
        temp_board = board.copy()                    # pass copy of playfield to computer
        temp_board[row][col] = opponent              # find winning play for player and place piece to block
        if winning_move(temp_board, opponent):       # if block also wins game for ai, retrun the winning play
            return col

    return random.choice(valid_locations)         # if block and win conditions impossible in 1 move, play a random valid move