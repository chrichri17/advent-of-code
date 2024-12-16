# https://adventofcode.com/2024/day/16
import heapq
import math
from collections import defaultdict, deque


def read_inputs(filepath):
    with open(filepath) as file:
        maze = [list(line) for line in file.read().strip().splitlines()]
        start = next(
            (r, c)
            for r, row in enumerate(maze)
            for c, cell in enumerate(row)
            if cell == "S"
        )
        return maze, start


# right, down, left, up (clockwise order)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def dijkstra(maze, start):
    """
    Hand-made implementation of dijkstra's algorithm

    See https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    """
    # Map<(r, c, direction), cost>
    DIST = defaultdict(lambda: math.inf)
    DIST[(*start, 0)] = 0
    # Map<(r, c, direction), set<(r, c, direction)>>
    PREV = defaultdict(set)

    pq = [(0, *start, 1)]  # cost, r, c, direction
    best_cost = math.inf

    while pq:
        cost, r, c, direction = heapq.heappop(pq)
        if cost > DIST[(r, c, direction)]:
            continue
        if maze[r][c] == "E":
            if cost > best_cost:
                break
            best_cost = cost

        dr, dc = DIRECTIONS[direction]
        for new_cost, nr, nc, d in [
            (cost + 1, r + dr, c + dc, direction),  # move forward
            (cost + 1000, r, c, (direction + 1) % 4),  # rotate clockwise
            (cost + 1000, r, c, (direction - 1) % 4),  # rotate counterclockwise
        ]:
            if maze[nr][nc] == "#":
                continue
            curr_cost = DIST[(nr, nc, d)]
            if new_cost > curr_cost:
                continue
            if new_cost < curr_cost:
                PREV[(nr, nc, d)] = set()  # clear previous paths
                DIST[(nr, nc, d)] = new_cost
            PREV[(nr, nc, d)].add((r, c, direction))
            heapq.heappush(pq, (new_cost, nr, nc, d))

    return best_cost, PREV


def get_tiles(maze, prev):
    q = deque([(r, c, d) for r, c, d in prev.keys() if maze[r][c] == "E"])
    seen = set()
    tiles = set()

    while q:
        r, c, d = q.popleft()
        if (r, c, d) in seen:
            continue
        seen.add((r, c, d))
        tiles.add((r, c))
        for pr, pc, pd in prev[(r, c, d)]:
            q.append((pr, pc, pd))
    return tiles


def main(filepath):
    maze, start = read_inputs(filepath)
    best_cost, prev = dijkstra(maze, start)
    tiles = get_tiles(maze, prev)
    print("Part 1:", best_cost)
    print("Part 2:", len(tiles))
