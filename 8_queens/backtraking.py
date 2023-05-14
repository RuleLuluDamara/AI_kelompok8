import time

def is_valid(board, row, col):
    n = len(board)
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

def n_queens(n):
    board = [-1] * n
    iteration = 0
    
    def solve(board, row):
        nonlocal iteration
        if row == n:
            return True
        for col in range(n):
            iteration += 1
            if is_valid(board, row, col):
                board[row] = col
                if solve(board, row + 1):
                    return True
        return False
    
    start_time = time.time()
    if solve(board, 0):
        end_time = time.time()
        print_board(board)
        print(f"Banyak iterasi: {iteration}")
        print(f"Waktu: {end_time - start_time} detik")
    else:
        print("Tidak ada solusi yang ditemukan")

def print_board(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)

n = 8
n_queens(n)
