# https://adventofcode.com/2021/day/19

from collections import deque
from copy import deepcopy


def read_inputs(filepath):
    with open(filepath) as file:
        scanners_raw = file.read().strip().split("\n\n")
        scanners = [
            {tuple(map(int, line.split(","))) for line in scanner.split("\n")[1:]}
            for scanner in scanners_raw
        ]
        return scanners


# Each scanner can:
#   1. Face any of 6 directions: +x, -x, +y, -y, +z, -z
#   2. Have 4 possible "up" directions once facing is chosen
#
# Here's why: Once you choose which axis direction the scanner is "facing" (6 choices), you still need to determine which direction is "up". The remaining two axes can be arranged in
# 4 ways while maintaining a right-handed coordinate system.
#  For example, if facing +x:
#   - Up can be +y (right is +z)
#   - Up can be -y (right is -z)
#   - Up can be +z (right is -y)
#   - Up can be -z (right is +y)
#
# These are just the 4 rotation on x-axis facing positive
#   +x --> (x, y, z) (x, z, -y) (x, -y, -z) (x, -z, y)
# Similarily, if facing -x:
#   -x --> (-x, -y, z) (-x, -z, y) (-x, y, -z) (-x, z, -y)
# and so on...


# The above gives us the following rotations
def rotate90(x, y, z):
    return (x, z, -y)


def rotate180(x, y, z):
    # Equivalent to rotate90(rotate90(origin))
    return (x, -y, -z)


def rotate270(x, y, z):
    # Equivalent to rotate90(rotate90(rotate90(origin)))
    return (x, -z, y)


# And the following transformers
def compose(f, g):
    return lambda x, y, z: g(*f(x, y, z))


fx = lambda x, y, z: (x, y, z)
fy = lambda x, y, z: (y, z, x)
fz = lambda x, y, z: (z, x, y)

fx_neg = lambda x, y, z: (-x, z, y)
fy_neg = lambda x, y, z: (-y, x, z)
fz_neg = lambda x, y, z: (-z, y, x)

transformers = [
    # Facing +x
    fx,
    compose(fx, rotate90),
    compose(fx, rotate180),
    compose(fx, rotate270),
    # facing -x
    fx_neg,
    compose(fx_neg, rotate90),
    compose(fx_neg, rotate180),
    compose(fx_neg, rotate270),
    # facing +y
    fy,
    compose(fy, rotate90),
    compose(fy, rotate180),
    compose(fy, rotate270),
    # facing -y
    fy_neg,
    compose(fy_neg, rotate90),
    compose(fy_neg, rotate180),
    compose(fy_neg, rotate270),
    # facing +z
    fz,
    compose(fz, rotate90),
    compose(fz, rotate180),
    compose(fz, rotate270),
    # facing -z
    fz_neg,
    compose(fz_neg, rotate90),
    compose(fz_neg, rotate180),
    compose(fz_neg, rotate270),
    # facing +z
    fz,
    compose(fz, rotate90),
    compose(fz, rotate180),
    compose(fz, rotate270),
    # facing -z
    fz_neg,
    compose(fz_neg, rotate90),
    compose(fz_neg, rotate180),
    compose(fz_neg, rotate270),
]


def rotations(scanner):
    return [{f(*beacon) for beacon in scanner} for f in transformers]


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def sub(a, b):
    return tuple(n - m for n, m in zip(a, b))


# This is a brute force approach that re-arranges the scanners in the new coordinates system
# and checks for overlaps between them.
def check_overlap(scanner1, scanner2, nb_common=12):
    for rotation in rotations(scanner2):
        # Scanner 1 is the reference scanner
        # We then iterate over each rotation of scanner2 to find the coordinates system with the most common seen beacons
        for beacon1 in scanner1:
            for beacon2 in rotation:
                offset = sub(beacon2, beacon1)
                # We shift all beacons in rotation by the offset
                shifted_scanner = {sub(beacon, offset) for beacon in rotation}
                intersection = scanner1 & shifted_scanner
                if len(intersection) >= nb_common:
                    return (offset, shifted_scanner)

    return (None, None)


def solve(filepath):
    scanners = read_inputs(filepath)
    state = deepcopy(scanners[0])
    offsets = []
    queue = deque(scanners[1:])

    while queue:
        offset, new_coords_sys = check_overlap(state, queue[0])
        if new_coords_sys:
            state |= new_coords_sys
            offsets.append(offset)
            queue.popleft()
        else:
            queue.append(queue.popleft())

    max_distance = 0

    for i, a in enumerate(offsets):
        for b in offsets[i + 1 :]:
            max_distance = max(max_distance, manhattan_distance(a, b))

    return max_distance, len(state)


def main(filepath):
    max_distance, count = solve(filepath)
    print("Part 1:", count)
    print("Part 2:", max_distance)
