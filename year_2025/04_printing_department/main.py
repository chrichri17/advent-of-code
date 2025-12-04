# https://adventofcode.com/2025/day/4

from itertools import product

Grid = list[list[str]]
Pos = tuple[int, int]


def read_inputs(filepath) -> Grid:
    with open(filepath) as file:
        return list(list(line.strip()) for line in file.readlines())


def accessible_rolls(grid: Grid) -> set[Pos]:
    rolls = set()
    nrows, ncols = len(grid), len(grid[0])

    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if char != "@":
                continue

            count = 0
            for dr, dc in product([-1, 0, 1], [-1, 0, 1]):
                if dr == dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < nrows and 0 <= nc < ncols and grid[nr][nc] == "@":
                    count += 1

            if count < 4:
                rolls.add((r, c))

    return rolls


def remove_rolls(grid: Grid, rolls: set[Pos]) -> int:
    for r, c in rolls:
        grid[r][c] = "."
    return len(rolls)


def solve(grid):
    rolls = accessible_rolls(grid)
    removed = initial_accessible = remove_rolls(grid, rolls)

    total_removed = removed

    while removed > 0:
        rolls = accessible_rolls(grid)
        removed = remove_rolls(grid, rolls)
        total_removed += removed

    return initial_accessible, total_removed


def main(filepath):
    grid = read_inputs(filepath)
    initial_accessible, total_removed = solve(grid)
    print("Part 1:", initial_accessible)
    print("Part 2:", total_removed)
