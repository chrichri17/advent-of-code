# https://adventofcode.com/2021/day/15

import heapq


def read_inputs(filepath):
    with open(filepath) as file:
        return [list(map(int, line.strip())) for line in file]


def grow(grid, nb_tiles):
    nr, nc = len(grid), len(grid[0])
    new_grid = [[0] * nb_tiles * nc for _ in range(nb_tiles * nr)]
    for r in range(nb_tiles * nr):
        for c in range(nb_tiles * nc):
            val = grid[r % nr][c % nc] + r // nr + c // nc
            if val >= 10:
                val = val % 9
            new_grid[r][c] = val
    return new_grid


def dijkstra(grid):
    nr, nc = len(grid), len(grid[0])
    pq = [(0, 0, 0)]
    seen = set()

    while pq:
        risk, r, c = heapq.heappop(pq)
        if (r, c) in seen:
            continue
        seen.add((r, c))
        if r == nr - 1 and c == nc - 1:
            return risk
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < nr and 0 <= cc < nc:
                heapq.heappush(pq, (risk + grid[rr][cc], rr, cc))


def solve(grid, nb_tiles=1):
    if nb_tiles == 1:
        return dijkstra(grid)
    return dijkstra(grow(grid, nb_tiles))


def main(filepath):
    grid = read_inputs(filepath)
    print("Part 1:", solve(grid))
    print("Part 2:", solve(grid, 5))
