#%%
from sudoku import print_grid, is_posible

grid = [[0, 0, 0, 7, 0, 0, 3, 0, 0],
        [0, 5, 2, 0, 4, 0, 0, 7, 6],
        [6, 0, 0, 5, 0, 0, 1, 0, 0],
        [0, 6, 0, 0, 0, 0, 7, 0, 8],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [9, 0, 4, 0, 0, 0, 0, 5, 0],
        [0, 0, 5, 0, 0, 3, 0, 0, 1],
        [3, 8, 0, 0, 6, 0, 4, 9, 0],
        [0, 0, 6, 0, 0, 1, 0, 0, 0],]


print("Is posible")
print_grid(grid)

n = 1
if is_posible(grid, n, 2, 7):
    print("Valid")
else:
    print("Failed")

n = 7
if is_posible(grid, n, 2, 7):
    print("Valid")
else:
    print("Failed")

n = 2
if not is_posible(grid, n, 2, 7):
    print("Valid")
else:
    print("Failed")

n = 5
if not is_posible(grid, n, 2, 7):
    print("Valid")
else:
    print("Failed")

n = 8
if not is_posible(grid, n, 2, 7):
    print("Valid")
else:
    print("Failed")


n = 3
if not is_posible(grid, n, 2, 7):
    print("Valid")
else:
    print("Failed")
# %%
