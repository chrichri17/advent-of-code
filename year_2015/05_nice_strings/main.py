# https://adventofcode.com/2015/day/5

from collections import Counter
from string import ascii_lowercase


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


def part1(filepath):
    count = 0
    for s in read_inputs(filepath):
        if (
            sum(1 for c in s if c in "aeiou") >= 3
            and any(a == b for a, b in zip(s, s[1:]))
            and all(sub not in s for sub in ["ab", "cd", "pq", "xy"])
        ):
            count += 1
    return count


def has_pair_twice(s: str) -> bool:
    counter = Counter()

    for i in range(1, len(s)):
        pair = s[i - 1] + s[i]
        if pair in counter:
            continue
        # s.count already returns the number of non-overlapping occurrences
        counter[pair] = s.count(pair)

    return any(v >= 2 for v in counter.values())


def part2(filepath):
    count = 0
    palindrom_3len = set(a + b + a for a in ascii_lowercase for b in ascii_lowercase)
    for s in read_inputs(filepath):
        if has_pair_twice(s) and any(p in s for p in palindrom_3len):
            count += 1
    return count


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
