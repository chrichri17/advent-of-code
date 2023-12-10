# https://adventofcode.com/2023/day/9

import re


def read_inputs(filepath):
    pattern = re.compile(r"(-?\d+)")
    with open(filepath) as file:
        for line in file.readlines():
            yield [int(i) for i in pattern.findall(line)]


def extrapolate(seq):
    if all(i == 0 for i in seq):
        return 0, 0
    diff = [b - a for a, b in zip(seq, seq[1:])]
    backward, forward = extrapolate(diff)
    return seq[0] - backward, forward + seq[-1]


def main(filepath):
    sequences = list(read_inputs(filepath))
    print("Part 1:", sum(forward for _, forward in map(extrapolate, sequences)))
    print("Part 2:", sum(backward for backward, _ in map(extrapolate, sequences)))
