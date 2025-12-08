# https://adventofcode.com/2025/day/8

import math
from collections import defaultdict
from pathlib import Path


# See https://www.geeksforgeeks.org/dsa/introduction-to-disjoint-set-data-structure-or-union-find-algorithm/
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def unite(self, i, j):
        irep = self.find(i)
        jrep = self.find(j)
        self.parent[irep] = jrep


def read_inputs(filepath):
    with open(filepath) as file:
        boxes = [tuple(map(int, line.strip().split(","))) for line in file.readlines()]
        N = len(boxes)
        distances = [
            (math.dist(boxes[i], boxes[j]), i, j)
            for i in range(N)
            for j in range(i + 1, N)
        ]
        distances.sort()
        return boxes, distances


def part1(boxes, distances, max_iter=10):
    uf = UnionFind(len(boxes))
    for idx in range(max_iter):
        _, i, j = distances[idx]
        uf.unite(i, j)
    sizes = defaultdict(int)
    for i in range(len(boxes)):
        sizes[uf.find(i)] += 1
    return math.prod(sorted(sizes.values())[-3:])


def part2(boxes, distances):
    uf = UnionFind(len(boxes))
    size = 1
    for _, i, j in distances:
        if uf.find(i) != uf.find(j):
            size += 1
            uf.unite(i, j)
        if size == len(boxes):
            return boxes[i][0] * boxes[j][0]


def main(filepath: Path):
    boxes, distances = read_inputs(filepath)
    max_iter = 10 if "test" in filepath.name else 1000
    print("Part 1:", part1(boxes, distances, max_iter=max_iter))
    print("Part 2:", part2(boxes, distances))
