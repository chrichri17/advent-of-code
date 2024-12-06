# https://adventofcode.com/2024/day/06


def read_inputs(filepath):
    with open(filepath) as file:
        grid = list(map(list, file.read().splitlines()))
        nrows, ncols = len(grid), len(grid[0])
        sr, sc = next(
            (r, c) for r in range(nrows) for c in range(ncols) if grid[r][c] == "^"
        )
        return grid, (sr, sc), (nrows, ncols)


class Directions:
    vectors = dict(
        U=(-1, 0),
        D=(1, 0),
        L=(0, -1),
        R=(0, 1),
    )
    directions = ["U", "R", "D", "L"]

    def __init__(self):
        self.pos = -1  # Next will be "U"

    def __next__(self):
        self.pos = (self.pos + 1) % 4
        return self.vectors[self.directions[self.pos]]


def patrol(grid, start):
    nr, nc = len(grid), len(grid[0])
    directions = Directions()

    r, c = start
    dr, dc = next(directions)
    has_loop = False
    history = set()
    seen = set()

    while True:
        r, c = r + dr, c + dc
        if (r, c, dr, dc) in history:
            has_loop = True
            break
        if not (0 <= r < nr and 0 <= c < nc):
            break
        if grid[r][c] == "#":
            r, c = r - dr, c - dc
            dr, dc = next(directions)
        history.add((r, c, dr, dc))
        seen.add((r, c))

    return seen, has_loop


def part1(filepath):
    grid, start, _ = read_inputs(filepath)
    seen, _ = patrol(grid, start)
    return len(seen)


# Takes a while to run for the input file
# A bit faster with pypy
def part2(filepath):
    grid, start, (nr, nc) = read_inputs(filepath)
    # (tips from @hyperneutrino): to make it faster, place obstacles on the guard path only: 32s -> 7s
    seen, _ = patrol(grid, start)
    count = 0
    for r in range(nr):
        for c in range(nc):
            if grid[r][c] != "." or (r, c) not in seen:
                continue
            grid[r][c] = "#"
            _, has_loop = patrol(grid, start)
            count += has_loop
            grid[r][c] = "."
    return count


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
