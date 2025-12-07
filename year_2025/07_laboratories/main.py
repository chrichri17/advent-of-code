# https://adventofcode.com/2025/day/7

from functools import lru_cache


def read_inputs(filepath):
    with open(filepath) as file:
        manifold = [list(line.strip()) for line in file.readlines()]
        sc = manifold[0].index("S")
        return manifold, (0, sc)


def part1(filepath):
    manifold, (sr, sc) = read_inputs(filepath)
    nrows, ncols = len(manifold), len(manifold[0])

    beams = {(sr, sc)}
    nb_split = 0

    while len(beams) > 0:
        new_beams = set()

        for r, c in beams:
            if r + 1 == nrows:
                continue
            nr, nc = r + 1, c
            if manifold[nr][nc] == "^":
                nb_split += 1
                if nc - 1 >= 0:
                    new_beams.add((nr, nc - 1))
                if nc + 1 < ncols:
                    new_beams.add((nr, nc + 1))
            else:
                new_beams.add((nr, nc))

        beams = new_beams

    return nb_split


def part2(filepath):
    manifold, (sr, sc) = read_inputs(filepath)
    nrows, ncols = len(manifold), len(manifold[0])

    @lru_cache(maxsize=None)
    def count_beams(r, c):
        if r + 1 == nrows:
            return 1

        nr, nc = r + 1, c
        if manifold[nr][nc] == "^":
            left_count = count_beams(nr, c - 1) if c - 1 >= 0 else 0
            right_count = count_beams(nr, c + 1) if c + 1 < ncols else 0
            return left_count + right_count
        else:
            return count_beams(nr, nc)

    return count_beams(sr, sc)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
