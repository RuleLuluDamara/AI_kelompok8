import time

def is_safe(board, row, col, N):
    # Cek baris di atas
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Cek diagonal atas kiri
    i = row - 1
    j = col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Cek diagonal atas kanan
    i = row - 1
    j = col + 1
    while i >= 0 and j < N:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True

def solve_n_queens(board, row, N, iterations):
    # Basis: semua baris sudah ditempati
    if row == N:
        return True

    # Iterasi untuk kolom pada baris saat ini
    for col in range(N):
        iterations[0] += 1
        if is_safe(board, row, col, N):
            # Tempatkan ratu di baris saat ini dan kolom yang dipilih
            board[row][col] = 1

            # Rekursif untuk menempatkan ratu pada baris selanjutnya
            if solve_n_queens(board, row + 1, N, iterations):
                return True

            # Jika tidak ada solusi yang ditemukan, ambil kembali langkah sebelumnya
            board[row][col] = 0

    return False

def print_board(board):
    N = len(board)
    for i in range(N):
        for j in range(N):
            print(board[i][j], end=" ")
        print()

def solve_n_queens_backtracking(initial_state):
    N = len(initial_state)
    # Inisialisai board 2D dengan dimensi NxN
    board = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            board[i][j] = initial_state[i][j]

    print("Initial state:")
    print_board(board)

    iterations = [0]
    start_time = time.time()

    if solve_n_queens(board, 0, N, iterations):
        end_time = time.time()
        print("\nGoal State:")
        print_board(board)
        print("Time:", end_time - start_time, "seconds")
        print("Iterations:", iterations[0])
    else:
        print("\nTidak ada solusi yang ditemukan.")

# Initial state yang diberikan
initial_state = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0]
]

solve_n_queens_backtracking(initial_state)
