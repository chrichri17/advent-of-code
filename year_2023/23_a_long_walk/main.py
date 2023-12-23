# https://adventofcode.com/2023/day/23

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

directions = {
    ".": [UP, DOWN, LEFT, RIGHT],
    "^": [UP],
    "v": [DOWN],
    "<": [LEFT],
    ">": [RIGHT],
}


def read_inputs(filepath):
    with open(filepath) as file:
        grid = file.read().splitlines()
        sr, sc = 0, grid[0].index(".")
        er, ec = len(grid) - 1, grid[-1].index(".")
        return grid, (sr, sc), (er, ec)


def get_neighbors(grid, r, c, climb_slopes=False):
    n, m = len(grid), len(grid[0])

    for dr, dc in directions["." if climb_slopes else grid[r][c]]:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != "#":
            yield nr, nc


def find_crossroads(grid, climb_slopes=False):
    crossroads = set()
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            if len(list(get_neighbors(grid, r, c, climb_slopes))) >= 3:
                crossroads.add((r, c))
    return crossroads


# Edge contraction to reduce the probelm size. Even with the reduced size, it's slow for part 2.
# https://en.wikipedia.org/wiki/Edge_contraction
def contract_edges(grid, start, end, climb_slopes=False):
    vertices = find_crossroads(grid)
    vertices.add(start)
    vertices.add(end)

    graph = {vertex: {} for vertex in vertices}

    for vertex in vertices:
        sr, sc = vertex
        stack = [(sr, sc, 0)]
        seen = set()

        while stack:
            r, c, dist = stack.pop()

            if (r, c) in seen:
                continue
            seen.add((r, c))

            if dist != 0 and (r, c) in vertices:
                graph[(sr, sc)][(r, c)] = dist
                continue

            for nr, nc in get_neighbors(grid, r, c, climb_slopes):
                stack.append((nr, nc, dist + 1))

    return graph


def find_longest_path_length(graph, start, end, seen=set()):
    if start == end:
        return 0

    max_length = 0

    seen.add(start)  # Mark as seen before exploring other paths

    for neighbor in graph[start]:
        if neighbor in seen:
            continue
        dist = graph[start][neighbor]
        max_length = max(
            max_length, find_longest_path_length(graph, neighbor, end) + dist
        )

    seen.remove(start)  # TO make sure it can get explored later
    return max_length


def solve(filepath, climb_slopes=False):
    grid, start, end = read_inputs(filepath)
    graph = contract_edges(grid, start, end, climb_slopes)
    return find_longest_path_length(graph, start, end)


def main(filepath):
    print("Part 1:", solve(filepath))
    print("Part 2:", solve(filepath, climb_slopes=True))
