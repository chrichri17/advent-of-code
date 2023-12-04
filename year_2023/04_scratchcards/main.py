# https://adventofcode.com/2023/day/4

import re


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            pattern = re.compile(r"(\d+)")
            s1, s2 = line.strip().split(":")[1].split(" | ")
            s1 = set(map(int, pattern.findall(s1)))
            s2 = set(map(int, pattern.findall(s2)))
            yield s1.intersection(s2)


def part1(filepath):
    return sum(2 ** (len(s) - 1) if len(s) else 0 for s in read_inputs(filepath))


def part2(filepath):
    match_counts = [len(s) for s in read_inputs(filepath)]
    scratchcards = [1] * len(match_counts)  # 1 for each original card

    for i, c in enumerate(match_counts):
        for j in range(1, c + 1):
            scratchcards[i + j] += scratchcards[i]

    return sum(scratchcards)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
