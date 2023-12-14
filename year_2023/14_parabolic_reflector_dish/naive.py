# https://adventofcode.com/2023/day/14

UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)


def read_inputs(filepath):
    with open(filepath) as file:
        grid = [list(line) for line in file.read().splitlines()]
        return grid


def pretty_print(grid):
    for row in grid:
        print("".join(row))


def in_bounds(grid, i, j, direction):
    n, m = len(grid), len(grid[0])
    if direction == UP:
        return i > 0
    elif direction == LEFT:
        return j > 0
    elif direction == DOWN:
        return i < n - 1
    elif direction == RIGHT:
        return j < m - 1


def slide_rocks(grid):
    grid = tuple(map("".join, zip(*grid)))
    grid = tuple(
        "#".join(
            ["".join(sorted(tuple(group), reverse=True)) for group in row.split("#")]
        )
        for row in grid
    )


def tilt(grid, i, j, direction=UP):
    current = grid[i][j]
    grid[i][j] = "."

    while in_bounds(grid, i, j, direction):
        x = i + direction[0]
        y = j + direction[1]
        if grid[x][y] != ".":
            break
        i, j = x, y
    grid[i][j] = current


def tilt_north(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "O":
                tilt(grid, r, c, UP)


def tilt_west(grid):
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if grid[r][c] == "O":
                tilt(grid, r, c, LEFT)


def tilt_south(grid):
    for r in range(len(grid) - 1, -1, -1):
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                tilt(grid, r, c, DOWN)


def tilt_east(grid):
    for c in range(len(grid[0]) - 1, -1, -1):
        for r in range(len(grid)):
            if grid[r][c] == "O":
                tilt(grid, r, c, RIGHT)


def cycle(grid):
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def get_load(grid):
    return sum((len(grid) - r) * row.count("O") for r, row in enumerate(grid))


def part1(filepath):
    grid = read_inputs(filepath)
    tilt_north(grid)
    return get_load(grid)


def part2(filepath):
    grid = read_inputs(filepath)
    cache = {}
    x = None

    for i in range(1, 1000000001):
        cycle(grid)
        key = "".join("".join(row) for row in grid)
        if key in cache:
            x = i
            break
        else:
            cache[key] = i

    cycle_length = x - cache[key]
    first_seen = cache[key] + (1000000000 - x) % cycle_length
    grid_repr = next(k for k, v in cache.items() if v == first_seen)
    # fmt: off
    grid = [
        list(grid_repr[i:i+len(grid)]) for i in range(0, len(grid_repr), len(grid))
    ]
    # fmt: on
    return get_load(grid)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
