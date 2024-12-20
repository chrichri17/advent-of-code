# https://adventofcode.com/2024/day/20

from collections import defaultdict, deque


def read_inputs(filepath):
    with open(filepath) as file:
        return [list(row.strip()) for row in file]


def bfs(grid, sr, sc):
    Q = deque([(sr, sc, 0)])
    DIST = defaultdict(lambda: -1)

    while Q:
        r, c, d = Q.popleft()
        if (r, c) in DIST:
            continue
        DIST[(r, c)] = d

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]) and grid[rr][cc] != "#":
                Q.append((rr, cc, d + 1))

    return DIST


def manhattan_neighbors(r, c, rad):
    neighbors = set()
    for dr in range(rad + 1):
        dc = rad - dr
        neighbors.add((r + dr, c + dc))
        neighbors.add((r + dr, c - dc))
        neighbors.add((r - dr, c + dc))
        neighbors.add((r - dr, c - dc))
    return neighbors


def solve(grid, max_cheat=2):
    assert max_cheat >= 2, "max_cheat must be at least 2"

    nr, nc = len(grid), len(grid[0])
    sr, sc = next((r, c) for r in range(nr) for c in range(nc) if grid[r][c] == "S")

    DIST = bfs(grid, sr, sc)

    cheats = defaultdict(set)

    for r in range(nr):
        for c in range(nc):
            if grid[r][c] == "#":
                continue

            for rad in range(2, max_cheat + 1):
                for cr, cc in manhattan_neighbors(r, c, rad):
                    d = DIST[(cr, cc)]
                    if cr < 0 or cr >= nr or cc < 0 or cc >= nc or d == -1:
                        continue
                    if d - DIST[(r, c)] >= 100 + rad:
                        cheats[d - DIST[(r, c)]].add(((r, c), (cr, cc)))

    return sum(len(v) for v in cheats.values())


def main(filepath):
    grid = read_inputs(filepath)
    print("Part 1:", solve(grid, max_cheat=2))
    print("Part 2:", solve(grid, max_cheat=20))
