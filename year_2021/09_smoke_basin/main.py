# https://adventofcode.com/2021/day/9
import heapq
import re
from collections import Counter, defaultdict, deque
from math import gcd, lcm, prod


def read_inputs(filepath):
    with open(filepath) as file:
        return [[int(h) for h in row] for row in file.read().splitlines()]


def get_lowpoints(heightmap):
    lowpoints = set()
    nrows, ncols = len(heightmap), len(heightmap[0])
    for r in range(nrows):
        for c in range(ncols):
            neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            if all(
                heightmap[nr][nc] > heightmap[r][c]
                for nr, nc in neighbors
                if 0 <= nr < nrows and 0 <= nc < ncols
            ):
                lowpoints.add((r, c))
    return lowpoints


def part1(filepath):
    heightmap = read_inputs(filepath)
    lowpoints = get_lowpoints(heightmap)
    return sum(1 + heightmap[r][c] for (r, c) in lowpoints)


def part2(filepath):
    heightmap = read_inputs(filepath)
    lowpoints = get_lowpoints(heightmap)
    nrows, ncols = len(heightmap), len(heightmap[0])
    basins_length = []

    for lp in lowpoints:
        Q = deque([lp])
        basin = {lp}

        while Q:
            r, c = Q.popleft()
            neightbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for nr, nc in neightbors:
                if 0 <= nr < nrows and 0 <= nc < ncols and heightmap[nr][nc] != 9:
                    if (nr, nc) not in basin and heightmap[nr][nc] > heightmap[r][c]:
                        basin.add((nr, nc))
                        Q.append((nr, nc))

        basins_length.append(len(basin))

    basins_length.sort(reverse=True)
    return prod(basins_length[:3])


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
