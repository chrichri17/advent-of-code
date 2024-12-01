# https://adventofcode.com/2024/day/1
from collections import Counter


def read_inputs(filepath):
    lloc, rloc = [], []
    with open(filepath) as file:
        for line in file.readlines():
            x, y = line.strip().split()
            lloc.append(int(x))
            rloc.append(int(y))
    return lloc, rloc


def part1(filepath):
    lloc, rloc = read_inputs(filepath)
    lloc.sort()
    rloc.sort()
    return sum(abs(a - b) for a, b in zip(lloc, rloc))


def part2(filepath):
    lloc, rloc = read_inputs(filepath)
    counter = Counter(rloc)
    return sum(map(lambda x: x * counter[x], lloc))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
