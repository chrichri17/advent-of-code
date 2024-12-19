# https://adventofcode.com/2024/day/19

from functools import lru_cache


def read_inputs(filepath):
    with open(filepath) as file:
        patterns, designs = file.read().strip().split("\n\n")
        patterns = patterns.strip().split(", ")
        designs = designs.strip().splitlines()
        return tuple(patterns), designs


@lru_cache
def ways(design, patterns):
    if len(design) == 0:
        return 1

    count = 0
    for pattern in patterns:
        if design.startswith(pattern):
            n = len(pattern)
            count += ways(design[n:], patterns)
    return count


def main(filepath):
    patterns, designs = read_inputs(filepath)
    all_ways = [ways(design, patterns) for design in designs]
    print("Part 1:", sum(1 for w in all_ways if w))
    print("Part 2:", sum(all_ways))
