# https://adventofcode.com/2023/day/11

from bisect import bisect_left


def read_inputs(filepath):
    empty_rows = []
    empty_cols = []
    galaxies = []
    with open(filepath) as file:
        image = list(map(list, file.read().strip().splitlines()))
        empty_rows = [r for r, row in enumerate(image) if set(row) == {"."}]
        empty_cols = [c for c, col in enumerate(zip(*image)) if set(col) == {"."}]
        galaxies = [
            (r, c)
            for r, row in enumerate(image)
            for c, ch in enumerate(row)
            if ch == "#"
        ]
        return galaxies, empty_rows, empty_cols


def expand_galaxies(
    galaxies: list[tuple[int, int]],
    empty_rows: list[int],
    empty_cols: list[int],
    size: int,
) -> list[tuple[int, int]]:
    new_galaxies = []
    for galaxy in galaxies:
        # how many rows are empty before this galaxy
        i = bisect_left(empty_rows, galaxy[0])
        # how many cols are empty before this galaxy
        j = bisect_left(empty_cols, galaxy[1])
        new_galaxies.append((i * size + galaxy[0], j * size + galaxy[1]))
    return new_galaxies


def solve(filepath, size=2):
    galaxies = expand_galaxies(*read_inputs(filepath), size - 1)
    total = 0

    for i in range(len(galaxies)):
        start = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            target = galaxies[j]
            total += abs(start[0] - target[0]) + abs(start[1] - target[1])

    return total


def main(filepath):
    print("Part 1:", solve(filepath, 2))
    print("Part 2:", solve(filepath, 1000000))
