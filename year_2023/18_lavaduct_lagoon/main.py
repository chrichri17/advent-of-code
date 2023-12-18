# https://adventofcode.com/2023/day/18

# using this is cheating, but it's so much easier than writing my own
from shapely import Polygon


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


dirs = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def part1(filepath):
    points = [(0, 0)]
    n = 0

    for line in read_inputs(filepath):
        direction, dist, _ = line.split()
        dist = int(dist)
        n += dist

        x, y = points[-1]
        dx, dy = dirs[direction]
        points.append((x + dx * dist, y + dy * dist))

    polygon = Polygon(points)
    # Shoelace used to compute polygon.area and Pick's theorem to count the number of points inside the polygon
    return int(polygon.area + n / 2 + 1)


def part2(filepath):
    points = [(0, 0)]
    n = 0

    for line in read_inputs(filepath):
        _, _, color = line.split()
        color = color[2:-1]
        direction = ["R", "D", "L", "U"][int(color[-1])]
        dist = int(color[:-1], 16)
        n += dist

        x, y = points[-1]
        dx, dy = dirs[direction]
        points.append((x + dx * dist, y + dy * dist))

    polygon = Polygon(points)
    return int(polygon.area + n / 2 + 1)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
