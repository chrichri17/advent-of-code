# https://adventofcode.com/2024/day/11
import re
from collections import defaultdict, deque, Counter
from math import prod, lcm, gcd
import heapq


def read_inputs(filepath):
    with open(filepath) as file:
        return [int(s) for s in file.read().split()]


def blink(stones, times=25):
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


def main(filepath):
    stones = read_inputs(filepath)
    print("Part 1:", blink(stones))
    print("Part 2:", blink(stones, 75))
