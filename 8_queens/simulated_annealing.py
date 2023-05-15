import random
import math
import time

# initialize board adalah program untuk membuat array 1 dimensi
# ukurannya adalah 8, tiap index melambangkan 1 kolom dari papan catur
# elemen dari array terdiri dari 0-7, ini melambangkan baris dari posisi queen


def initialize_board():
    board = [0]*8
    for i in range(8):
        board[i] = random.randint(0, 7)
    return board


# memindahkan posisi queens ke posisi yang baru
def randomize(board):
    new_board = list(board)
    i = random.randint(0, 7)
    j = random.randint(0, 7)
    new_board[i] = j
    return new_board

# objective function, untuk mencari jumlah pasangan queen yang saling menyerang


def Attacking_Queen(board):
    Queen = 0
    for i in range(8):
        for j in range(i+1, 8):
            if board[i] == board[j] or abs(i-j) == abs(board[i]-board[j]):
                Queen += 1
    return Queen


# algoritma sim_annealing
def simulated_annealing():
    start_time = time.time()
    board = initialize_board()
    temperature = 100
    cooling_rate = 0.99
    iteration = 0

    while temperature > 0.00001:
        new_board = randomize(board)
        delta = Attacking_Queen(new_board) - Attacking_Queen(board)

        if delta < 0:
            board = new_board
        else:
            if random.random() < math.exp(-delta/temperature):
                board = new_board

        temperature *= cooling_rate
        iteration += 1

        # Check if the board is already solved
        if Attacking_Queen(board) == 0:
            break

    end_time = time.time()
    print(f"Total iterations: {iteration}")
    print(f"Time taken to finish: {end_time - start_time:.5f} seconds")
    att = Attacking_Queen(board)
    print(f"Number of attacking queens: {att}")

    result_board = [[0]*8 for _ in range(8)]
    for i in range(8):
        result_board[board[i]][i] = 1

    return result_board


def main():
    result = simulated_annealing()
    for row in result:
        print(row)


if __name__ == '__main__':
    main()
