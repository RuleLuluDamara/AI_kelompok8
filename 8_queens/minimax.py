def evaluate_state(board):
    # Mengevaluasi kondisi board saat ini, return 1 jika kondisi menang,
    # return -1 jika kondisi kalahse.

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row] == board[col] and row != col:
                return -1  # Queens saling mengancam secara horizontal, Kondisi kalah
            if abs(board[row] - board[col]) == abs(row - col) and row != col:
                return -1  # Queens saling mengancam secara vertikal, Kondisi kalah
    return 1  # Kondisi Menang


def generate_moves(board, row):
    # Generate semua kemungkinan pergerakan pada baris yang sudah ditentukan
    moves = []
    for col in range(len(board)):
        if board[row] == -1:
            moves.append(col)
    return moves


def minimax(board, depth, maximizing_player):
    # Mengaplikasikan minimax algorithm 
    if depth == 0:
        return evaluate_state(board)
    
    if maximizing_player:
        max_score = float('-inf')
        moves = generate_moves(board, depth - 1)
        for move in moves:
            new_board = board[:]
            new_board[depth - 1] = move
            score = minimax(new_board, depth - 1, False)
            max_score = max(max_score, score)
        return max_score
    else:
        min_score = float('inf')
        moves = generate_moves(board, depth - 1)
        for move in moves:
            new_board = board[:]
            new_board[depth - 1] = move
            score = minimax(new_board, depth - 1, True)
            min_score = min(min_score, score)
        return min_score


def solve_eight_queens():
    board = [-1] * 8  # Inisaliasi Board dengan cell kosong
    solve(board, 0)
    return board


def solve(board, row):
    if row == len(board):
        return True

    for col in range(len(board)):
        if is_safe(board, row, col):
            board[row] = col
            if solve(board, row + 1):
                return True
            board[row] = -1

    return False


def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
            return False
    return True


def print_board(board):
    for row in range(len(board)):
        line = ""
        for col in range(len(board)):
            if col == board[row]:
                line += "Q "
            else:
                line += "- "
        print(line)


def main():
    solution = solve_eight_queens()
    if solution:
        print("Solution:")
        print_board(solution)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()

