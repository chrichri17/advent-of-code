# https://adventofcode.com/2024/day/12
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass


def read_inputs(filepath):
    with open(filepath) as file:
        return file.read().strip().splitlines()


Point = namedtuple("Point", ["x", "y"])


@dataclass
class Region:
    # Crop value
    crop: str
    # Points in the region
    points: set[Point]
    # Horizontal boundaries: row -> set of points on the given horizontal bound
    rbounds: dict[int, set[Point]]
    # Vertical boundaries: column -> set of points on the given vertical bound
    cbounds: dict[int, set[Point]]

    @property
    def area(self):
        return len(self.points)

    @property
    def perimeter(self):
        hperimeter = sum(len(bound) for bound in self.rbounds.values())
        vperimeter = sum(len(bound) for bound in self.cbounds.values())
        return hperimeter + vperimeter

    @property
    def sides(self):
        hsides = self.horizontal_sides()
        vsides = self.vertical_sides()
        # print(hsides, vsides)
        return sum(hsides.values()) + sum(vsides.values())

    def horizontal_sides(self):
        sides = {}  # using dict for debugging purposes. We could just store the count
        for pos, rb in self.rbounds.items():
            count = 1
            rb = sorted(rb)
            for i in range(1, len(rb)):
                # new row => increase side count
                if rb[i][0] != rb[i - 1][0]:
                    count += 1
                # same row but not adjacent (i.e holes) => increase side count
                elif rb[i][1] - rb[i - 1][1] > 1:
                    count += 1
            sides[pos] = count
        return sides

    def vertical_sides(self):
        sides = {}  # using dict for debugging purposes. We could just store the count
        for pos, cb in self.cbounds.items():
            count = 1
            cb = sorted(cb, key=lambda x: (x[1], x[0]))
            for i in range(1, len(cb)):
                # new column => increase side count
                if cb[i][1] != cb[i - 1][1]:
                    count += 1
                # same column but not adjacent (i.e holes) => increase side count
                elif cb[i][0] - cb[i - 1][0] > 1:
                    count += 1
            sides[pos] = count
        return sides


def get_regions(grid) -> list[Region]:
    nrows, ncols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    regions = []
    seen = set()

    for r, row in enumerate(grid):
        for c, crop in enumerate(row):
            if (r, c) in seen:
                continue
            Q = deque([(r, c)])
            points = {(r, c)}
            rbounds = defaultdict(set)
            cbounds = defaultdict(set)

            while Q:
                cr, cc = Q.popleft()
                if (cr, cc) in seen:
                    continue
                seen.add((cr, cc))

                for dr, dc in directions:
                    nr, nc = cr + dr, cc + dc
                    if nr < 0 or nr >= nrows:
                        rbounds[nr].add((cr, cc))
                    elif nc < 0 or nc >= ncols:
                        cbounds[nc].add((cr, cc))
                    elif grid[nr][nc] != crop:
                        if dr == 0:
                            cbounds[nc].add((cr, cc))
                        else:
                            rbounds[nr].add((cr, cc))
                    else:
                        Q.append((nr, nc))
                        points.add((nr, nc))

            regions.append(Region(crop, points, rbounds, cbounds))

    return regions


def main(filepath):
    grid = read_inputs(filepath)
    regions = get_regions(grid)
    print("Part 1:", sum(r.area * r.perimeter for r in regions))
    print("Part 2:", sum(r.area * r.sides for r in regions))
