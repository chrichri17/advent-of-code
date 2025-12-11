# https://adventofcode.com/2025/day/11

from collections import deque
from functools import lru_cache


def read_inputs(filepath):
    with open(filepath) as file:
        nodes = {}
        for line in file.readlines():
            n, *neighbors = line.strip().replace(":", "").split()
            nodes[n] = neighbors
        return nodes


def part1(filepath):
    nodes = read_inputs(filepath)

    start = "you"
    end = "out"

    count = 0
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node == end:
            count += 1
            continue
        for neigh in nodes[node]:
            queue.append(neigh)

    return count


def part2(filepath):
    nodes = read_inputs(filepath)

    start = "svr"
    end = "out"

    @lru_cache(maxsize=None)
    def count_paths(node: str, fft=False, dac=False):
        if node == end:
            return int(fft and dac)
        return sum(
            count_paths(n, fft or n == "fft", dac or n == "dac") for n in nodes[node]
        )

    return count_paths(start)


def main(filepath):
    if "test1" in filepath.name:
        print("Part 1:", part1(filepath))
    if "test2" in filepath.name:
        print("Part 2:", part2(filepath))
    if "in" in filepath.name:
        print("Part 1:", part1(filepath))
        print("Part 2:", part2(filepath))
