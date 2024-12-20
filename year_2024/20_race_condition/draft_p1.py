import re
from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import permutations
from math import log2

# import networkx as nx
# from shapely import LinearRing, Polygon

data = open(0).read()

grid = [list(line) for line in data.splitlines()]

nr, nc = len(grid), len(grid[0])
# print(grid)

start = (0, 0)
end = (0, 0)
for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell == "S":
            start = (r, c)
        if cell == "E":
            end = (r, c)


path = []

Q = deque([(start, [start])])
seen = set()
corners = set()

while Q:
    node, p = Q.popleft()
    if node == end:
        path = p
        break

    if node in seen:
        continue
    seen.add(node)

    r, c = node
    count = 0
    x, y = 0, 0
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < nr and 0 <= cc < nc and grid[rr][cc] != "#":
            if dr == 0:
                x += grid[rr][cc] == "."
            else:
                y += grid[rr][cc] == "."
            Q.append(((rr, cc), p + [(rr, cc)]))
    if x == 1 and y == 1:
        # print("corner", r, c)
        corners.add((r, c))


saved_times = defaultdict(int)


# corners.add(start)
# corners.add(end)
# max_picoseconds = 0


def saved(a, b, c, d):
    i = 0
    j = 0
    for x, (rr, cc) in enumerate(path):
        if (rr, cc) == (a, b):
            i = x
        if (rr, cc) == (c, d):
            j = x
    return max(i, j) - min(i, j) - 2


# for r, c in corners:
#     if (r + 2, c) in corners and r + 2 < nc and grid[r + 1][c] == "#":
#         saved_time = saved(r, c, r + 2, c)
#         print("saved", r, c, r + 2, c, saved_time)
#         saved_times[saved_time] += 1
#         max_picoseconds = max(max_picoseconds, saved_time)
#     if (r, c + 2) in corners and c + 2 < nr and grid[r][c + 1] == "#":
#         saved_time = saved(r, c, r, c + 2)
#         print("saved", r, c, r, c + 2, saved_time)
#         max_picoseconds = max(max_picoseconds, saved_time)
#         saved_times[saved_time] += 1
# break


for r, row in enumerate(grid):
    if r == 0 or r == nr - 1:
        continue
    for c, cell in enumerate(row):
        if c == 0 or c == nc - 1:
            continue
        if cell != "#":
            continue

        if grid[r][c - 1] != "#" and grid[r][c + 1] != "#":
            saved_time = saved(r, c - 1, r, c + 1)
            saved_times[saved_time] += 1
        if grid[r - 1][c] != "#" and grid[r + 1][c] != "#":
            saved_time = saved(r - 1, c, r + 1, c)
            saved_times[saved_time] += 1

print(saved_times)
print(sum(v for k, v in saved_times.items() if k >= 100))
# print(len(corners))
# print(path)
