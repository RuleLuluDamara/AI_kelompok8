from copy import deepcopy # membuat salinan dari variabel domains dan constraints
import time

def print_board(board):
    for row in board:
        print(" ".join(row))

# memeriksa apakah menempatkan queens diposisi yang valid atau tidak
def is_valid(board, row, col, n, constraints):
    for i in range(n): # memeriksa baris dan kolom
        if board[row][i] == "Q" or board[i][col] == "Q":
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)): # memeriksa diagonal kiri atas - kanan bawah
        if board[i][j] == "Q":
            return False
    for i, j in zip(range(row, -1, -1), range(col, n)): # memeriksa diagonal kanan atas - kiri bawah 
        if board[i][j] == "Q":
            return False
    for c in constraints[row][col]: # memeriksa constraint yang menyimpan posisi tidak valid queens
        i, j = c
        if board[i][j] == "Q":
            return False # jika sudah terisi
    return True

def forward_checking(board, row, domains, constraints):
    global iterations
    iterations += 1
    if row == len(board):
        return True
    for col in domains[row]:
        if is_valid(board, row, col, len(board), constraints):
            board[row][col] = "Q"
            # membuat duplikat dari domains dan constraints untuk digunakan pada recursive call berikutnya.
            new_domains = deepcopy(domains) 
            new_constraints = deepcopy(constraints) 
            for i in range(row + 1, len(board)):
                # mengurangi domain setiap kotak pada baris yang tersisa setelah baris saat ini.
                if col in new_domains[i]:
                    new_domains[i].remove(col)
                    j = col + (i - row)
                    if j in new_domains[i]:
                        new_domains[i].remove(j)    
                    j = col - (i - row)
                    if j in new_domains[i]:
                        new_domains[i].remove(j)
                # mencari constraint yang terdapat pada kotak (i, col) dan diagonal yang bersesuaian dengan kotak yang baru saja diisi
                if (i, col) in new_constraints[i][col]:
                    new_constraints[i][col].remove((i, col))
                j = col + (i - row)
                if j >= 0 and j < len(board) and (i, j) in new_constraints[i][col]:
                    new_constraints[i][col].remove((i, j))
                j = col - (i - row)
                if j >= 0 and j < len(board) and (i, j) in new_constraints[i][col]:
                    new_constraints[i][col].remove((i, j))
            if forward_checking(board, row + 1, new_domains, new_constraints): # recursive call
                return True
            # backtrack
            board[row][col] = "."
            for i in range(row + 1, len(board)):
                if col not in domains[i]:
                    domains[i].add(col)
                    j = col + (i - row)
                    if j < len(board) and j not in domains[i]:
                        domains[i].add(j)    
                    j = col - (i - row)
                    if j >= 0 and j not in domains[i]:
                        domains[i].add(j)
                if (i, col) not in constraints[i][col]:
                    constraints[i][col].add((i, col))
                j = col + (i - row)
                if j >= 0 and j < len(board) and (i, j) not in constraints[i][col]:
                    constraints[i][col].add((i, j))
                j = col - (i - row)
                if j >= 0 and j < len(board) and (i, j) not in constraints[i][col]:
                    constraints[i][col].add((i, j))
    return False

def n_queens(n, constraints=[]):
    global iterations
    iterations = 0
    board = [["." for i in range(n)] for j in range(n)]
    domains = [set(range(n)) for i in range(n)]
    if not constraints:
        constraints = [[set() for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if k != j:
                        constraints[i][j].add((i, k))
                    if k != i:
                        constraints[i][j].add((k, j))
                    if k != 0 and i-k >= 0 and j-k >= 0:
                        constraints[i][j].add((i-k, j-k))
                    if k != 0 and i-k >= 0 and j+k < n:
                        constraints[i][j].add((i-k, j+k))
    start_time = time.time()
    if forward_checking(board, 0, domains, constraints):
        print_board(board)
    else:
        print("Tidak ada solusi yang ditemukan")
        
    end_time = time.time()
    print("Banyak iterasi:", iterations)
    print("Waktu :", end_time - start_time)   

n = 8
n_queens(n)

