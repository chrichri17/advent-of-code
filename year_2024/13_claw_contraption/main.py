# https://adventofcode.com/2024/day/13
import re


def read_inputs(filepath):
    pattern = re.compile(r"(\d+)")
    with open(filepath) as file:
        for block in file.read().strip().split("\n\n"):
            yield list(map(int, pattern.findall(block)))


def count_tokens(x1, y1, x2, y2, x, y):
    determinant = x1 * y2 - x2 * y1
    if determinant == 0:
        return 0

    a = (x * y2 - y * x2) / determinant
    b = (x1 * y - y1 * x) / determinant
    if is_int(a) and is_int(b):
        a, b = int(a), int(b)
        return 3 * a + b
    return 0


def is_int(x):
    return x - int(x) < 1e-9


def part1(filepath):
    return sum(count_tokens(*data) for data in read_inputs(filepath))


def part2(filepath):
    tX = tY = 10_000_000_000_000
    return sum(
        count_tokens(*data, tX + x, tY + y) for *data, x, y in read_inputs(filepath)
    )


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
