# https://adventofcode.com/2015/day/02

import heapq
import re
from collections import Counter, defaultdict, deque
from math import gcd, lcm, prod


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield tuple(map(int, line.strip().split("x")))


def part1(filepath):
    return sum(
        min(l * w, l * h, w * h) + 2 * (l * w + l * h + w * h)
        for l, w, h in read_inputs(filepath)
    )


def part2(filepath):
    return sum(
        l * w * h + 2 * min(l + w, l + h, w + h) for l, w, h in read_inputs(filepath)
    )


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
