# https://adventofcode.com/2024/day/18

from collections import deque
from pathlib import Path


def read_inputs(filepath: Path):
    M = 7  # max coords in x and y direction
    B = 12  # number first fallen bytes
    if filepath.stem == "in":
        M, B = 71, 1024

    with open(filepath) as file:
        coords = [tuple(map(int, line.strip().split(","))) for line in file.readlines()]
        grid = [["."] * M for _ in range(M)]

        assert B < len(coords)

        # Fall the first B bytes
        for i in range(B):
            x, y = coords[i]
            grid[y][x] = "#"

        return grid, M, coords, B


def find_exit(grid, M):
    start = (0, 0)
    end = (M - 1, M - 1)

    Q = deque([(start, 0)])
    seen = set()

    while Q:
        pos, count = Q.popleft()
        if pos == end:
            return count
        if pos in seen:
            continue
        seen.add(pos)

        x, y = pos
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < M and 0 <= ny < M and grid[ny][nx] == ".":
                Q.append(((nx, ny), count + 1))

    return -1


def part1(filepath: Path):
    grid, M, *_ = read_inputs(filepath)
    return find_exit(grid, M)


# A bit slow but fast enough for the contest
def part2(filepath: Path):
    grid, M, coords, B = read_inputs(filepath)
    for i in range(B, len(coords)):
        x, y = coords[i]
        grid[y][x] = "#"
        if find_exit(grid, M) == -1:
            return f"{x},{y}"


def main(filepath: Path):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
