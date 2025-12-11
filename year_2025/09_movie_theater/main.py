# https://adventofcode.com/2025/day/9

from shapely import Polygon, box

Point = tuple[int, int]


def read_inputs(filepath) -> list[Point]:
    with open(filepath) as file:
        return [tuple(map(int, line.strip().split(","))) for line in file.readlines()]  # pyright: ignore[reportReturnType]


def find_largest_area_outside(points: list[Point]) -> int:
    areas = [
        abs(x1 - x2 + 1) * abs(y1 - y2 + 1)
        for i, (x1, y1) in enumerate(points)
        for (x2, y2) in points[i + 1 :]
    ]
    return max(areas)


# This simplifies the problem by using shapely
# Not the real spiriti of AoC
# Hard way will be in draft.py
def find_largest_area_inside(points: list[Point]) -> int:
    poly = Polygon(points)
    best = 0
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[i + 1 :]:
            xm = min(x1, x2)
            xM = max(x1, x2)
            ym = min(y1, y2)
            yM = max(y1, y2)
            rect = box(xm, ym, xM, yM)
            # use covers instead of contains
            # covers checks for boundaries but contains does not
            if poly.covers(rect):
                best = max(best, abs(xM - xm + 1) * abs(yM - ym + 1))
    return best


def main(filepath):
    points = read_inputs(filepath)
    print("Part 1:", find_largest_area_outside(points))
    print("Part 2:", find_largest_area_inside(points))
