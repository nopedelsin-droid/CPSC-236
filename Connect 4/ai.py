import random

ROW_COUNT = 6
COL_COUNT = 7

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_valid_locations(board):
    return [col for col in range(COL_COUNT) if is_valid_location(board, col)]

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Standard 4-in-a-row check
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)): return True
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)): return True
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)): return True
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)): return True
    return False

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    opponent = 1 if piece == 2 else 2

    # 1. Check for immediate win
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        temp_board[row][col] = piece
        if winning_move(temp_board, piece):
            return col

    # 2. Check for immediate block
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        temp_board[row][col] = opponent
        if winning_move(temp_board, opponent):
            return col

    return random.choice(valid_locations)