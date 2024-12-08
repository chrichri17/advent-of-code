# https://adventofcode.com/2024/day/08
from collections import defaultdict


def read_inputs(filepath):
    with open(filepath) as file:
        return list(map(list, file.read().splitlines()))


def get_impact(grid, unlimited=False):
    antennas = defaultdict(list)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                antennas[cell].append((r, c))

    antinodes = set()
    bounds = (len(grid), len(grid[0]))
    for _, locations in antennas.items():
        antinodes |= get_antinodes(locations, bounds, unlimited)
    return len(antinodes)


def get_antinodes(locations, bounds, unlimited=False):
    antinodes = set()
    nrows, ncols = bounds
    for i, (r1, c1) in enumerate(locations):
        for _, (r2, c2) in enumerate(locations[i + 1 :]):
            dr = r2 - r1
            dc = c2 - c1

            a, b = r1 - dr, c1 - dc
            while 0 <= a < nrows and 0 <= b < ncols:
                antinodes.add((a, b))
                if not unlimited:  # Part 1
                    break
                a -= dr
                b -= dc

            c, d = r2 + dr, c2 + dc
            while 0 <= c < nrows and 0 <= d < ncols:
                antinodes.add((c, d))
                if not unlimited:  # Part 1
                    break
                c += dr
                d += dc
            if unlimited:
                antinodes.add((r1, c1))
                antinodes.add((r2, c2))
    return antinodes


def main(filepath):
    grid = read_inputs(filepath)
    print("Part 1:", get_impact(grid))
    print("Part 2:", get_impact(grid, unlimited=True))
