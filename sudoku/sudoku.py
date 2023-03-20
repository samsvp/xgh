# %%
from functools import reduce
from typing import *


SUDOKU_NUMBERS = set(range(1, 10))


def print_grid(grid: List[List[int]]):
    """Prints the current grid"""
    grid_str = ""
    def add_line(grid_str: str) -> str:
        grid_str += " |"
        for x in range(11):
            grid_str += " -"
        grid_str += " |\n"
        return grid_str

    #grid_str = add_line(grid_str)
    for y in range(9):
        if y % 3 == 0: 
            grid_str = add_line(grid_str)
        for x in range(9):
            grid_str += f"{'' if x % 3 else ' |'} {grid[y][x]}"
        grid_str += " |\n"

    grid_str = add_line(grid_str)
    
    print(grid_str)


def is_posible(grid: List[List[int]], n: int, x: int, y: int) -> bool:
    """Checks if you can add the number 'n' at position (x,y)"""
    row = grid[y]
    column = [grid[_y][x] for _y in range(9)]
    # return if we can't add it because the number appear at its row or column
    if any(n==_n for _n in row): return False
    if any(n==_n for _n in column): return False

    x = x//3*3 + 1
    y = y//3*3 + 1
    # check if number appear inside square
    return not any(
        grid[y + yy][x + xx] == n
        for yy in range(-1, 2)
        for xx in range(-1, 2))


def possible_numbers(grid: List[List[int]], x: int, y: int) -> Set[int]:
    """Returns all possible numbers at the given position"""
    if grid[y][x]: return set()
    
    row = grid[y]
    column = [grid[_y][x] for _y in range(9)]
    x = x//3*3 + 1
    y = y//3*3 + 1
    box = [grid[y + yy][x + xx] 
        for yy in range(-1, 2)
        for xx in range(-1, 2)]

    return SUDOKU_NUMBERS.difference(set(row) | set(column) | set(box))


def guarantied_numbers_box(bx: int, by: int,
        pn: Dict[Tuple[int, int], Set[int]]) -> List[Set[int]]:
    """Returns the guarantied numbers inside all the squares in the box coordinates"""
    pn, indexes = zip(*[
        (pn[(x, y)], (x, y))
        for y in range(3 * by, 3 * by + 3)
        for x in range(3 * bx, 3 * bx + 3)])
    
    possible_new = {}
    for i in range(9):
        pn_copy = list(pn).copy()
        possible = pn_copy.pop(i)
        if not possible: possible_new[indexes[i]] = possible

        all_p = reduce(lambda a, b: a | b, pn_copy)
        possible_new[indexes[i]] = possible.difference(all_p)
    return possible_new


def possible_rows(possible_numbers: Dict[Tuple[int, int], Set[int]], 
                 n: int, bx: int, by: int) -> Set[int]:
    """Returns all the rows that the given number can be in"""
    pr = []
    for y in range(3 * by, 3 * by + 3 ):
        for x in range(3 * bx, 3 * bx + 3 ):
            if n not in possible_numbers[(x, y)]:
                continue
            
            pr.append(y)
            break
    return set(pr)


def possible_columns(possible_numbers: Dict[Tuple[int, int], Set[int]], 
                 n: int, bx: int, by: int) -> Set[int]:
    """Returns all the columns that the given number can be in"""
    pr = []
    for x in range(3 * bx, 3 * bx + 3 ):
        for y in range(3 * by, 3 * by + 3 ):
            if n not in possible_numbers[(x, y)]:
                continue
            
            pr.append(x)
            break
    return set(pr)


def possible_numbers_box(grid: List[List[int]], bx: int, by: int, 
        pn: Dict[Tuple[int, int], Set[int]]) -> List[Set[int]]:
    """Returns the possible numbers inside all the squares in the box coordinates"""
    pnb = { 
        (x, y): possible_numbers(grid, x, y)
        for y in range(3 * by, 3 * by + 3)
        for x in range(3 * bx, 3 * bx + 3)
    }

    return pnb


def solve_by_rule(grid: List[List[int]]):
    """Tries to solve by placing numbers which are guarantied to be 
    in the right place"""
    changed = False
    pn = { 
        (x, y): possible_numbers(grid, x, y)
        for y in range(9)
        for x in range(9)
    }

    for y in range(3):
        for x in range(3):
            pn.update(possible_numbers_box(grid, x, y, pn))
            
    for x in range(3):
        for y in range(3):
            numbers = guarantied_numbers_box(x, y, pn)
            for k, v in numbers.items():
                if not v: continue
                changed = True
                grid[k[1]][k[0]] = list(v)[0]
                break
    if changed:
        solve_by_rule(grid)
    else:
        print_grid(grid)


def brute_solver(grid: List[List[int]]):
    """A brute force solver using recursion"""
    for y in range(9):
        for x in range(9):
            if grid[y][x]: continue

            for n in range(1, 10):
                if not is_posible(grid, n, x, y): continue

                grid[y][x] = n
                brute_solver(grid)
                grid[y][x] = 0
            return

    print_grid(grid)



#%%
if __name__ == "__main__":
    grid = [[0, 0, 0, 7, 0, 0, 3, 0, 0],
        [0, 5, 2, 0, 4, 0, 0, 7, 6],
        [6, 0, 0, 5, 0, 0, 1, 0, 0],
        [0, 6, 0, 0, 0, 0, 7, 0, 8],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [9, 0, 4, 0, 0, 0, 0, 5, 0],
        [0, 0, 5, 0, 0, 3, 0, 0, 1],
        [3, 8, 0, 0, 6, 0, 4, 9, 0],
        [0, 0, 6, 0, 0, 1, 0, 0, 0],]
    
    brute_solver(grid)

    for x in range(9):
        y = 0
        print(f"posible numbers at ({x}, {y}): {possible_numbers(grid, x, y)}")

    solve_by_rule(grid)
    # import time
    # grid = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 9, 0, 0, 1, 0, 0, 3, 0],
    #     [0, 0, 6, 0, 2, 0, 7, 0, 0],
    #     [0, 0, 0, 3, 0, 4, 0, 0, 0],
    #     [2, 1, 0, 0, 0, 0, 0, 9, 8],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 2, 5, 0, 6, 4, 0, 0],
    #     [0, 8, 0, 0, 0, 0, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],]

    # s = time.time()    
    # brute_solver(grid)
    # print(time.time() - s)

    import time
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9],]

    s = time.time()
    solve_by_rule(grid)
    brute_solver(grid)
    print(time.time() - s)
# %%
