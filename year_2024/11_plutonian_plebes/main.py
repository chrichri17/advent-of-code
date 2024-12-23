# https://adventofcode.com/2024/day/11
from collections import Counter
from functools import cache


def read_inputs(filepath):
    with open(filepath) as file:
        return [int(s) for s in file.read().split()]


def solve(stones, times=25):
    counter = Counter(stones)
    for _ in range(times):
        new_counter = Counter()
        for s, count in counter.items():
            if s == 0:
                new_counter[1] += count
            elif len(str(s)) % 2 == 0:
                mid = len(str(s)) // 2
                new_counter[int(str(s)[:mid])] += count
                new_counter[int(str(s)[mid:])] += count
            else:
                new_counter[s * 2024] += count
        counter = new_counter
    return sum(counter.values())


@cache
def count_stones(stone, times=25):
    if times == 0:
        return 1

    if stone == 0:
        return count_stones(1, times - 1)
    if len(str(stone)) % 2 == 0:
        mid = len(str(stone)) // 2
        return count_stones(int(str(stone)[:mid]), times - 1) + count_stones(
            int(str(stone)[mid:]), times - 1
        )
    return count_stones(stone * 2024, times - 1)


# Recursive version
def solve(stones, times=25):
    return sum(count_stones(s, times) for s in stones)


def main(filepath):
    stones = read_inputs(filepath)
    print("Part 1:", solve(stones))
    print("Part 2:", solve(stones, 75))
