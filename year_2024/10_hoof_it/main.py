# https://adventofcode.com/2024/day/9
from collections import deque


def read_inputs(filepath):
    with open(filepath) as file:
        return [[int(x) for x in row] for row in file.read().splitlines()]


def find_all_paths(grid):
    nrows, ncols = len(grid), len(grid[0])
    all_paths = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != 0:
                continue
            Q = deque([(r, c, 0, [])])
            paths = []
            while Q:
                rr, cc, val, path = Q.popleft()
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < nrows and 0 <= nc < ncols and grid[nr][nc] == val + 1:
                        if grid[nr][nc] == 9:
                            paths.append(path + [(nr, nc)])
                        else:
                            Q.append((nr, nc, val + 1, path + [(nr, nc)]))
            all_paths[(r, c)] = paths
    return all_paths


def part1(filepath):
    grid = read_inputs(filepath)
    all_paths = find_all_paths(grid)
    return sum(len(set(path[-1] for path in paths)) for paths in all_paths.values())


def part2(filepath):
    grid = read_inputs(filepath)
    all_paths = find_all_paths(grid)
    return sum(len(paths) for paths in all_paths.values())


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
