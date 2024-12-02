# https://adventofcode.com/2021/day/06
from collections import Counter, defaultdict


def read_inputs(filepath):
    with open(filepath) as file:
        return list(map(int, file.read().strip().split(",")))


def next_day(fishes: defaultdict[int, int]) -> defaultdict[int, int]:
    next_fishes = defaultdict(int)
    for k, v in fishes.items():
        if k == 0:
            next_fishes[6] += v
            next_fishes[8] += v
        else:
            next_fishes[k - 1] += v
    return next_fishes


def simulate(
    fishes: defaultdict[int, int], days: int
) -> tuple[defaultdict[int, int], int]:
    for _ in range(days):
        fishes = next_day(fishes)
    return fishes, sum(fishes.values())


def main(filepath):
    lantern_fishes = Counter(read_inputs(filepath))
    print("Part 1:", simulate(lantern_fishes, 80)[1])
    print("Part 2:", simulate(lantern_fishes, 256)[1])
