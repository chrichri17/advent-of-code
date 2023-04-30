from collections import deque
from typing import Generator


Heightmap = list[list[str]]
Square = tuple[int, int]


def read_inputs(filepath: str) -> tuple[Heightmap, Square, Square]:
    heightmap = []
    source: Square = None
    target: Square = None

    with open(filepath) as file:
        for i, line in enumerate(file.readlines()):
            heightmap.append(list(line.strip()))
            for j, square in enumerate(heightmap[-1]):
                if square == "S":
                    source = (i, j)
                    # normalize the input: S behaves like a
                    heightmap[i][j] = "a"
                elif square == "E":
                    target = (i, j)
                    # normalize the input: E behaves like z
                    heightmap[i][j] = "z"

    return heightmap, source, target


def get_neighbors(
    heightmap: Heightmap, square: Square, desc: bool = False
) -> Generator[Square, None, None]:
    n, m = len(heightmap), len(heightmap[0])
    i, j = square
    incr = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for x, y in incr:
        p, q = x + i, y + j
        if 0 <= p < n and 0 <= q < m:
            diff = ord(heightmap[p][q]) - ord(heightmap[i][j])
            if (desc is True and diff >= -1) or (desc is False and diff <= 1):
                yield (p, q)


def shortest_path_steps(
    heightmap: Heightmap, source: Square, target: str | Square
) -> int:
    desc = True if isinstance(target, str) else False

    def is_end(square: Square):
        if isinstance(target, str):
            x, y = square
            return heightmap[x][y] == target
        return square == target

    steps = {source: 0}
    queue: deque[Square] = deque([source])

    # run bfs
    while len(queue) > 0:
        node = queue.popleft()
        for neighbor in get_neighbors(heightmap, node, desc):
            if is_end(neighbor):
                return steps[node] + 1
            elif neighbor in steps:
                continue
            else:
                steps[neighbor] = steps[node] + 1
                queue.append(neighbor)

    return -1


def main(filepath: str):
    heightmap, source, target = read_inputs(filepath)
    print("Part 1:", shortest_path_steps(heightmap, source, target))
    print("Part 2:", shortest_path_steps(heightmap, target, "a"))
