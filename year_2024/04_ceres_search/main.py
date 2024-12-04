# https://adventofcode.com/2024/day/04


def read_inputs(filepath):
    with open(filepath) as file:
        grid = list(list(line) for line in file.read().splitlines())
        return grid, len(grid), len(grid[0])


DIRECTIONS = [
    # Horizontal
    (0, 1),
    (0, -1),
    # Vertical
    (1, 0),
    (-1, 0),
    # Diagonal x + y = cte
    (1, 1),
    (-1, -1),
    # Diagonal x - y = cte
    (1, -1),
    (-1, 1),
]


def part1(filepath):
    grid, R, C = read_inputs(filepath)

    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != "X":
                continue
            for dr, dc in DIRECTIONS:
                if 0 <= r + 3 * dr < R and 0 <= c + 3 * dc < C:
                    val = "".join(grid[r + k * dr][c + k * dc] for k in range(4))
                    count += val == "XMAS" or val == "SAMX"
    return count


def part2(filepath):
    grid, R, C = read_inputs(filepath)
    # M . M     M . S     S . M     S . S
    # . A .     . A .     . A .     . A .
    # S . S     M . S     S . M     M . M
    possible_corners = ["MMSS", "MSMS", "SMSM", "SSMM"]
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != "A":
                continue
            corners = [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
            if not all(0 <= x < R and 0 <= y < C for x, y in corners):
                continue
            corners = "".join(grid[x][y] for x, y in corners)
            count += corners in possible_corners
    return count


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
