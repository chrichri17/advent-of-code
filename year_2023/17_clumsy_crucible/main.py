# https://adventofcode.com/2023/day/17

from heapq import heappop, heappush
from typing import Union

Direction = tuple[int, int]

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


DIRECTIONS: list[Direction] = [UP, DOWN, LEFT, RIGHT]

Heatmap = list[list[int]]


def read_inputs(filepath) -> Heatmap:
    with open(filepath) as file:
        return [list(map(int, line)) for line in file.read().splitlines()]


# Shortest path revisited
def dijkstra(heatmap: Heatmap, min_before_turn=0, max_without_turn=3):
    n, m = len(heatmap), len(heatmap[0])
    src = (0, 0)
    target = (n - 1, m - 1)

    visited = set()
    # heat_loss, (x, y), direction | None, count
    pq = [(0, src, None, 0)]

    while pq:
        heat_loss, (x, y), direction, count = heappop(pq)
        if (x, y) == target and count >= min_before_turn:
            return heat_loss

        if (x, y, direction, count) in visited:
            continue
        visited.add((x, y, direction, count))

        for nx, ny, nd, c in get_neighbors(
            x, y, direction, count, min_before_turn, max_without_turn
        ):
            if (nx, ny, nd, c) in visited:
                continue
            if 0 <= nx < n and 0 <= ny < m:
                heappush(pq, (heat_loss + heatmap[nx][ny], (nx, ny), nd, c))


def get_neighbors(
    x: int,
    y: int,
    direction: Union[Direction, None],
    count: int,
    min_before_turn=0,
    max_without_turn=3,
):
    if direction is None:
        return [(x + dx, y + dy, (dx, dy), 1) for dx, dy in DIRECTIONS]

    dx, dy = direction

    # Make sure we don't turn too early
    if count < min_before_turn:
        return [(x + dx, y + dy, direction, count + 1)]

    neighbors = []

    # Make sure we don't go straight for too long
    if count < max_without_turn:
        neighbors.append((x + dx, y + dy, direction, count + 1))

    for ndx, ndy in DIRECTIONS:
        # We can't go back or keep the same direction
        if (ndx, ndy) != (dx, dy) and (ndx, ndy) != (-dx, -dy):
            neighbors.append((x + ndx, y + ndy, (ndx, ndy), 1))

    return neighbors


def main(filepath):
    heatmap = read_inputs(filepath)
    print("Part 1:", dijkstra(heatmap))
    print("Part 2:", dijkstra(heatmap, 4, 10))
