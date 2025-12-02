# https://adventofcode.com/2021/day/5
import re
from collections import defaultdict

Point = tuple[int, int]


def print_grid(points: dict[Point, int], *bounds):
    mr, Mr, mc, Mc = bounds

    for y in range(mc, Mc + 1):
        for x in range(mr, Mr + 1):
            print(points.get((x, y), "."), end=" ")
        print()


def read_inputs(filepath):
    lines = []
    mr, Mr, mc, Mc = 0, 0, 0, 0
    with open(filepath) as file:
        for line in file.readlines():
            x1, y1, x2, y2 = map(int, re.findall(r"(\d+)", line))
            lines.append((x1, y1, x2, y2))
            mr = min(mr, x1, x2)
            Mr = max(Mr, x1, x2)
            mc = min(mc, y1, y2)
            Mc = max(Mc, y1, y2)
    return lines, (mr, Mr, mc, Mc)


def mark_points(
    points: defaultdict[Point, int], line: tuple[int, int, int, int], skip_diagonal=True
):
    x1, y1, x2, y2 = line
    dx = x2 - x1
    dy = y2 - y1
    if (dx != 0 and dy != 0) and skip_diagonal:
        return

    if dx:
        dx = dx // abs(dx)
    if dy:
        dy = dy // abs(dy)

    x, y = x1, y1
    while True:
        points[(x, y)] += 1
        if (x, y) == (x2, y2):
            break
        x += dx
        y += dy


def part1(filepath):
    points = defaultdict(int)
    lines, bounds = read_inputs(filepath)
    for line in lines:
        mark_points(points, line)
    # print_grid(points, *bounds)
    return sum(1 for v in points.values() if v > 1)


def part2(filepath):
    points = defaultdict(int)
    lines, bounds = read_inputs(filepath)
    for line in lines:
        mark_points(points, line, False)
    # print_grid(points, *bounds)
    return sum(1 for v in points.values() if v > 1)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
