from copy import deepcopy
import time

def print_board(board):
    for row in board:
        print(" ".join(row))

def is_valid(board, row, col, n, constraints):
    # Melakukan iterasi untuk setiap kolom dalam baris yang sama dengan row
    for i in range(n):
        if board[row][i] == "1" or board[i][col] == "1":
            return False
    # Melakukan iterasi diagonal ke arah kiri atas
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == "1":
            return False
    # Melakukan iterasi diagonal ke arah kanan atas
    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j] == "1":
            return False
    # Melakukan iterasi untuk setiap konstrain 
    for c in constraints[row][col]:
        i, j = c
        if board[i][j] == "1":
            return False
    return True

def forward_checking(board, row, domains, constraints):
    global iterations
    iterations += 1
    if row == len(board):
        return True
    for col in domains[row]:
        if is_valid(board, row, col, len(board), constraints):
            board[row][col] = "1"
            new_domains = deepcopy(domains) # Membuat salinan domain kolom (domains) 
            new_constraints = deepcopy(constraints) # Membuat salinan konstrain penempatan queen (constraints)
            
            for i in range(row + 1, len(board)):
                # Jika kolom yang sedang diperiksa (col) masih ada dalam domain kolom (new_domains)
                # maka kolom tersebut harus dihapus dari domain baris i , karena konflik vertikal terjadi.
                if col in new_domains[i]:
                    new_domains[i].remove(col)
                    j = col + (i - row) #  Menghitung indeks kolom untuk pengecekan konflik diagonal kanan-bawah
                    if j in new_domains[i]:
                        new_domains[i].remove(j) # Hapus new_domains karena terjadi konflik diagonal kanan-bawah
                    j = col - (i - row) #  Menghitung indeks kolom untuk pengecekan konflik diagonal kiri-bawah
                    if j in new_domains[i]:
                        new_domains[i].remove(j) ## Hapus new_domains karena terjadi konflik diagonal kiri-bawah
                if (i, col) in new_constraints[i][col]:
                    # Jika posisi masih ada dalam konstrain penempatan queen
                    # maka harus dihapus dari konstrain tersebut.
                    new_constraints[i][col].remove((i, col)) 
                j = col + (i - row)
                if j >= 0 and j < len(board) and (i, j) in new_constraints[i][col]:
                    new_constraints[i][col].remove((i, j))
                j = col - (i - row)
                if j >= 0 and j < len(board) and (i, j) in new_constraints[i][col]:
                    new_constraints[i][col].remove((i, j))

            if forward_checking(board, row + 1, new_domains, new_constraints): # recursive call
                return True
            # Jika pemanggilan rekursif tidak menghasilkan solusi yang valid
            # maka queen yang ditempatkan pada baris row dan kolom col dihapus 
            # dari papan catur dengan mengubah nilainya menjadi "0".
            board[row][col] = "0"
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


def n_queens(n, constraints=[], initial_state=None):
    global iterations
    iterations = 0
    board = [["0" for i in range(n)] for j in range(n)]
    domains = [set(range(n)) for i in range(n)]

    if initial_state is not None:
        for i in range(n):
            for j in range(n):
                if initial_state[i][j] == "1":
                    board[i][j] = "1"
                    domains[i] = set()
                    constraints[i][j] = set()
                    for k in range(n):
                        if k != j:
                            constraints[i][k].add((i, k))
                        if k != i:
                            constraints[k][j].add((k, j))
                        if i - k >= 0 and j - k >= 0:
                            constraints[i - k][j - k].add((i - k, j - k))
                        if i - k >= 0 and j + k < n:
                            constraints[i - k][j + k].add((i - k, j + k))

    if not constraints:
        constraints = [[set() for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if k != j:
                        constraints[i][j].add((i, k))
                    if k != i:
                        constraints[i][j].add((k, j))
                    if k != 0 and i - k >= 0 and j - k >= 0:
                        constraints[i][j].add((i - k, j - k))
                    if k != 0 and i - k >= 0 and j + k < n:
                        constraints[i][j].add((i - k, j + k))

    start_time = time.time()
    if forward_checking(board, 0, domains, constraints):
        print_board(board)
    else:
        print("Tidak ada solusi yang ditemukan")

    end_time = time.time()
    print("Banyak iterasi:", iterations)
    print("Waktu :", end_time - start_time)


n = 8
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
n_queens(n, initial_state=initial_state)

