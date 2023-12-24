# https://adventofcode.com/2023/day/24

from collections import namedtuple
from typing import Union

from sympy import solve, symbols

Hailstone = namedtuple("Hailstone", "x y z vx vy vz")


def read_inputs(filepath):
    hailstones = []
    with open(filepath) as file:
        for line in file.readlines():
            hailstones.append(
                Hailstone(*list(map(int, line.replace(" @ ", ", ").split(", "))))
            )
    return hailstones


def intersect(a: Hailstone, b: Hailstone) -> Union[tuple[float, float, float], None]:
    # Stone path equation: y = c * (x - x0) + y0 with c = vy / vx
    ca = a.vy / a.vx
    cb = b.vy / b.vx

    if ca == cb:
        return None

    sx = (cb * b.x - ca * a.x - (b.y - a.y)) / (cb - ca)
    sy = ca * (sx - a.x) + a.y
    t = min(
        (sx - a.x) / a.vx,
        (sx - b.x) / b.vx,
    )
    return sx, sy, t


def part1(filepath):
    lo, hi = 200_000_000_000_000, 400_000_000_000_000
    if "test" in str(filepath):
        lo, hi = 7, 27

    hailstones = read_inputs(filepath)
    count = 0
    for j, b in enumerate(hailstones):
        for i in range(j):
            a = hailstones[i]
            intersection = intersect(a, b)
            if intersection is None:
                continue
            sx, sy, t = intersection
            if lo <= sx <= hi and lo <= sy <= hi and t >= 0:
                count += 1

    return count


def part2(filepath):
    hailstones = read_inputs(filepath)
    x, y, z, vx, vy, vz = symbols("x y z vx vy vz")
    equations = []

    # Take enough values to have a singleton
    for a in hailstones[:4]:
        # Using x + t * vx = xa + t * va_x
        # and z + t * vz = za + t * va_z, we can remove t from the system and get the equation below
        equations.append((vz - a.vz) * (a.x - x) - (vx - a.vx) * (a.z - z))
        # We do the same for x and y
        equations.append((vy - a.vy) * (a.x - x) - (vx - a.vx) * (a.y - y))

    solutions = solve(equations)
    assert len(solutions) == 1

    solution = solutions[0]
    return solution[x] + solution[y] + solution[z]


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
