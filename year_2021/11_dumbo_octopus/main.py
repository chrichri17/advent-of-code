# https://adventofcode.com/2021/day/11
from collections import deque


def read_inputs(filepath):
    with open(filepath) as file:
        return [[int(o) for o in row] for row in file.read().splitlines()]


def step(grid):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    nrows, ncols = len(grid), len(grid[0])
    flashes = set()

    for r in range(nrows):
        for c in range(ncols):
            grid[r][c] += 1
            if grid[r][c] == 10:
                flashes.add((r, c))

    Q = deque(flashes)
    visited = set()

    while Q:
        r, c = Q.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < nrows and 0 <= nc < ncols:
                grid[nr][nc] += 1
                if grid[nr][nc] >= 10:
                    Q.append((nr, nc))

    count = 0
    for r in range(nrows):
        for c in range(ncols):
            if grid[r][c] >= 10:
                grid[r][c] = 0
                count += 1

    return grid, count


def part1(filepath):
    grid = read_inputs(filepath)
    count = 0
    for _ in range(100):
        grid, c = step(grid)
        count += c
    return count


def part2(filepath):
    grid = read_inputs(filepath)
    nrows, ncols = len(grid), len(grid[0])
    count = i = 0
    while count < nrows * ncols:
        grid, count = step(grid)
        i += 1
    return i


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
