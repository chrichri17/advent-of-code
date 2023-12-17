UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def read_inputs(filepath) -> list[str]:
    with open(filepath) as file:
        return file.read().splitlines()


def count_energized(
    contraption: list[str], start: tuple[int, int, tuple[int, int]]
) -> int:
    n, m = len(contraption), len(contraption[0])
    beams = [start]
    seen = set()

    while beams:
        new_beams = []

        for x, y, direction in beams:
            if x < 0 or x >= n or y < 0 or y >= m:
                continue

            if (x, y, direction) in seen:
                continue
            seen.add((x, y, direction))

            dx, dy = direction

            tile = contraption[x][y]
            # Continue in the same direction for empty space or pointy end of a splitter
            if tile == "." or (tile == "-" and dx == 0) or (tile == "|" and dy == 0):
                new_beams.append((x + dx, y + dy, direction))
            elif tile == "/":
                # Flip direction along the line y = -x
                dx, dy = -dy, -dx
                new_beams.append((x + dx, y + dy, (dx, dy)))
            elif tile == "\\":
                # Flip direction along the line y = x
                dx, dy = dy, dx
                new_beams.append((x + dx, y + dy, (dx, dy)))
            else:
                # Split in two when the beam encounters the flat side of a splitter
                for ndx, ndy in [LEFT, RIGHT] if tile == "-" else [UP, DOWN]:
                    new_beams.append((x + ndx, y + ndy, (ndx, ndy)))

        beams = new_beams

    return len({(x, y) for x, y, _ in seen})


def part1(filepath):
    contraption = read_inputs(filepath)
    return count_energized(contraption, (0, 0, RIGHT))


def part2(filepath):
    contraption = read_inputs(filepath)
    n, m = len(contraption), len(contraption[0])

    count = 0
    for r in range(n):
        count = max(count, count_energized(contraption, (r, 0, RIGHT)))
        count = max(count, count_energized(contraption, (r, m - 1, LEFT)))

    for c in range(m):
        count = max(count, count_energized(contraption, (0, c, DOWN)))
        count = max(count, count_energized(contraption, (n - 1, c, UP)))

    return count


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
