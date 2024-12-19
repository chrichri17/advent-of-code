# https://adventofcode.com/2024/day/16
import re
from collections import defaultdict, deque, Counter
import math
import heapq
from pathlib import Path


class Bathroom:
    def __init__(self, width, height, robots):
        self.w = width
        self.h = height
        self.initial_state = robots[:]
        self.robots = robots

    @property
    def quadrants(self):
        wm = self.w // 2
        hm = self.h // 2
        tl = tr = bl = br = 0

        for px, py, *_ in self.robots:
            if px < wm and py < hm:
                tl += 1
            elif px > wm and py < hm:
                tr += 1
            elif px < wm and py > hm:
                bl += 1
            elif px > wm and py > hm:
                br += 1

        return tl, tr, bl, br

    def show(self, fn=lambda x: str(x)):
        grid = self._empty_grid()
        for x, y, *_ in self.robots:
            grid[y][x] += 1
        for row in grid:
            print("".join(fn(x) if x else "." for x in row))
        print()

    def predict(self, seconds):
        for i, (x, y, vx, vy) in enumerate(self.initial_state):
            nx = (x + vx * seconds) % self.w
            ny = (y + vy * seconds) % self.h
            self.robots[i] = (nx, ny, vx, vy)

    def entropy(self):
        grid = self._empty_grid()

        count = 0
        for px, py, *_ in self.robots:
            grid[py][px] += 1
            count += 1

        def shannon(x, y):
            pi = grid[y][x] / count
            return pi * math.log2(pi) if pi else 0

        return sum(
            shannon(x, y) for y, row in enumerate(grid) for x, _ in enumerate(row)
        )

    def _empty_grid(self):
        return [[0 for _ in range(self.w)] for _ in range(self.h)]

    def _neighbors8(self, x, y):
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    neighbors.append((nx, ny))
        return neighbors


def read_inputs(filepath: Path):
    pattern = re.compile(r"(-?\d+)")

    width, height = 11, 7
    if filepath.stem == "in":
        width, height = 101, 103

    robots = []

    with open(filepath) as file:
        for line in file.readlines():
            robots.append(list(map(int, pattern.findall(line))))

    return Bathroom(width, height, robots)


def show(robots, width, height, fn=lambda x: str(x)):
    grid = [[0 for _ in range(width)] for _ in range(height)]

    for p in robots:
        px = int(p[0])
        py = int(p[1])
        grid[py][px] += 1

    for row in grid:
        print("".join(fn(x) if x else "." for x in row))
    print()


def part1(filepath):
    bathroom = read_inputs(filepath)
    # bathroom.show()
    bathroom.predict(100)
    # bathroom.show()
    return math.prod(bathroom.quadrants)


# Could also be solved with a BFS to find out robots that are connected.
def part2(filepath):
    bathroom = read_inputs(filepath)

    best_elapsed = 0
    min_entropy = math.inf

    # Stop after w * h because the robots teleport themselves.
    # At that point, we know we've reached a cycle.
    for seconds in range(bathroom.w * bathroom.h):
        bathroom.predict(seconds)

        entropy = bathroom.entropy()
        if entropy < min_entropy:
            min_entropy = entropy
            best_elapsed = seconds

    # bathroom.predict(best_elapsed)
    # bathroom.show(fn=lambda _: "#")

    return best_elapsed


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
