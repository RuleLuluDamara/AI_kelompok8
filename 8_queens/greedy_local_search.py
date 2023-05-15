import random
import time

def generate_board():
    board = [0]*8
    for i in range(8):
        board[i] = random.randint(0, 7)
    col = random.randint(0, 7)
    row = board[col]
    board[col] = random.randint(0, 7)
    board[row] = col
    print("Initial board:")
    visualize_board(board)
    # print("\n\n")
    return board

def user_input():
    board = [0]*8
    for i in range(8):
        board[i] = int(input(f"Enter queen position for row {i+1}: "))
    print("Initial board:")
    visualize_board(board)
    print("\n\n")
    return board

def count_conflicts(board):
    conflicts = 0
    for i in range(8):
        for j in range(i+1, 8):
            if board[i] == board[j]:
                conflicts += 1
            offset = j - i
            if board[i] == board[j] - offset or board[i] == board[j] + offset:
                conflicts += 1
    return conflicts

total_iterations = 0
def get_best_move(board):
    global total_iterations
    best_moves = []
    current_conflicts = count_conflicts(board)
    for col in range(8):
        for row in range(8):
            if board[col] == row:
                # print(f"Queen at column {col} || {board[col]} || is already in row {row}")
                continue
            board_copy = list(board)
            board_copy[col] = row
            new_conflicts = count_conflicts(board_copy)
            total_iterations += 1
            print("iteration:", total_iterations)
            if new_conflicts < current_conflicts:
                current_conflicts = new_conflicts
                best_moves = [(col,row)]
            elif new_conflicts == current_conflicts:
                best_moves.append((col,row))
    return random.choice(best_moves)

def visualize_board(board):
    for row in range(8):
        line = ""
        for col in range(8):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)

def solve():
    global total_iterations
    # board = generate_board()
    board = user_input()
    start_time = time.time()
    while True:
        conflicts = count_conflicts(board)
        print("Conflicts:", conflicts)
        if conflicts == 0:
            print("Solution found in", total_iterations, "iterations:")
            visualize_board(board)
            end_time = time.time()
            print("Time taken:", end_time - start_time, "seconds")
            return
        col, row = get_best_move(board)
        board[col] = row
        visualize_board(board)
        # print("\n")

solve()

# 2 3 2 6 7 1 7 4