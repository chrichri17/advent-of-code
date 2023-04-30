import re
from typing import Generator


def read_inputs(filename) -> Generator[tuple[int], None, None]:
    pattern = "-?\d+"

    with open(filename) as file:
        for line in file.readlines():
            yield tuple(map(int, re.findall(pattern, line)))


def get_impossible_spots(
    inputs: list[tuple[int]], lineno: int
) -> tuple[list[tuple[int, int]], set[int]]:
    beacons = set()
    intervals = []

    # Fetch first the possible intervals, I.e
    # the possible x-pos for a beacon with y == lineno
    for sx, sy, bx, by in inputs:
        dist = abs(sx - bx) + abs(sy - by)
        delta = dist - abs(sy - lineno)

        if delta < 0:
            continue
        if by == lineno:
            beacons.add(bx)
        intervals.append((sx - delta, sx + delta))

    # merge all the intervals as much as possible.
    intervals.sort()
    lo, hi = intervals[0]
    merged = []

    for m, M in intervals[1:]:
        if m <= hi + 1 and M >= hi + 1:
            # update the current interval
            hi = M
        elif m > hi + 1:
            # add the previous reduced interval
            merged.append((lo, hi))
            # track a new reduced interval
            lo, hi = m, M

    merged.append((lo, hi))
    return merged, beacons


def count_impossible_spots(inputs: list[tuple[int]], lineno: int) -> int:
    intervals, beacons = get_impossible_spots(inputs, lineno)
    count = lambda interval: interval[1] - interval[0] + 1
    return sum(map(count, intervals)) - len(beacons)


def find_distress_beacon_freq(inputs: list[tuple[int]], limit: int) -> int:
    COEF = 4_000_000

    # Takes a bit of time since O(4_000_000 * n) where n = len(inputs)
    for y in range(limit + 1):
        intervals, _ = get_impossible_spots(inputs, y)
        if len(intervals) != 2:
            continue
        (_, hi), (lo, _) = intervals
        if hi + 1 != lo - 1:
            raise ValueError("weird inputs")
        return COEF * (hi + 1) + y


def main(filename):
    inputs = list(read_inputs(filename))
    lineno = 10
    if filename.name.startswith("in"):
        lineno = 2_000_000
    limit = lineno * 2
    print("Part 1:", count_impossible_spots(inputs, lineno))
    print("Part 2:", find_distress_beacon_freq(inputs, limit))
