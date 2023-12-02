# https://adventofcode.com/2023/day/2

# Trying to use one-liners although it can harm readability
from math import prod


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield parse_game(line.strip())


def parse_game(line: str) -> tuple[int, list[dict[str, int]]]:
    no, _, subsets = line[5:].partition(": ")
    return int(no), [
        {c: int(n) for n, c in (cube.split(" ") for cube in subset.split(", "))}
        for subset in subsets.split("; ")
    ]


def possible_games_sum(filepath) -> int:
    bag = dict(red=12, green=13, blue=14)

    def validate_subset(subset):
        return all(subset.get(k, 0) <= v for k, v in bag.items())

    return sum(
        no
        for no, subsets in read_inputs(filepath)
        if all(validate_subset(subset) for subset in subsets)
    )


def power_sets_sum(filepath) -> int:
    return sum(
        prod(
            max(subset.get(k, 0) for subset in subsets)
            for k in ["red", "green", "blue"]
        )
        for _, subsets in read_inputs(filepath)
    )


def main(filepath):
    print("Part 1:", possible_games_sum(filepath))
    print("Part 2:", power_sets_sum(filepath))
