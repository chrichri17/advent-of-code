# https://adventofcode.com/2023/day/14


def read_inputs(filepath):
    with open(filepath) as file:
        return file.read().splitlines()


def pprint(grid):
    for row in grid:
        print("".join(row))


def tilt_north(grid):
    grid = list(map("".join, zip(*grid)))  # Transpose the grid
    grid = tilt_west(grid)
    grid = list(map("".join, zip(*grid)))  # Transpose the grid back
    return grid


def tilt_west(grid):
    new_grid = []
    for row in grid:
        # Split by group and sort each group (using #) with the O's first:
        #   ..O#.O.#. will become O..#O..#.
        new_row = "#".join(
            "".join(sorted(group, reverse=True)) for group in row.split("#")
        )
        new_grid.append(new_row)
    return new_grid


def tilt_south(grid):
    return tilt_north(grid[::-1])[::-1]  # Reverse cols (to be in North case)


def tilt_east(grid):
    grid = tilt_west([row[::-1] for row in grid])  # Reverse rows (to be in West case)
    grid = [row[::-1] for row in grid]  # Reverse back
    return grid


def cycle(grid):
    grid = tilt_north(grid)
    grid = tilt_west(grid)
    grid = tilt_south(grid)
    grid = tilt_east(grid)
    return grid


def get_load(grid):
    return sum((len(grid) - r) * row.count("O") for r, row in enumerate(grid))


def part1(filepath):
    grid = read_inputs(filepath)
    grid = tilt_north(grid)
    return get_load(grid)


def part2(filepath):
    N = 1_000_000_000
    grid = read_inputs(filepath)
    cache = {}
    x = None

    for i in range(1, N + 1):
        grid = cycle(grid)
        key = tuple(grid)
        if key in cache:
            x = i
            break
        else:
            cache[key] = i

    cycle_length = x - cache[key]
    first_seen = cache[key] + (N - x) % cycle_length
    grid = list(next(k for k, v in cache.items() if v == first_seen))
    return get_load(grid)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
