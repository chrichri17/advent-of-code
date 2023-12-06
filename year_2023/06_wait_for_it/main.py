# https://adventofcode.com/2023/day/6

import re
from math import prod


def read_inputs(filepath):
    pattern = re.compile(r"(\d+)")
    with open(filepath) as file:
        return pattern.findall(file.readline()), pattern.findall(file.readline())


def get_wins(time: int, distance: int) -> int:
    wins = 0
    for j in range(time):
        dist = j * (time - j)
        if dist > distance:
            wins += 1
    return wins


def part1(filepath):
    times, distances = read_inputs(filepath)
    times = list(map(int, times))
    distances = list(map(int, distances))
    return prod(get_wins(time, distances[i]) for i, time in enumerate(times))


# Runs in ~3s for puzzle inputs
def part2(filepath):
    times, distances = read_inputs(filepath)
    time = int("".join(times))
    distance = int("".join(distances))
    return get_wins(time, distance)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
