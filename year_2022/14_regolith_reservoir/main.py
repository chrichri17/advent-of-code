from typing import Generator

Path = list[tuple[int, int]]


def read_inputs(filepath: str) -> Generator[Path, None, None]:
    with open(filepath) as file:
        for line in file.readlines():
            yield list(map(lambda s: tuple(map(int, s.split(","))), line.split(" -> ")))


def parse_inputs(paths: list[Path]) -> tuple[set[complex], int]:
    rocks: set[complex] = set()
    y_max = 0

    for path in paths:
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))

            y_max = max(y_max, y2)

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    rocks.add(x + y * 1j)

    return rocks, y_max


def drop_sand_until_abyss(
    rocks: set[complex], y_max: int, pouring_point: complex = 500
):
    """
    Simulate the falling sand until it starts flowing into the abyss
    """
    sand_units = 0
    visited = set(rocks)

    while True:
        pos = pouring_point

        while True:
            if pos.imag >= y_max:
                return sand_units

            # Move the sand down or down-left or down-right
            if pos + 1j not in visited:
                pos += 1j
            elif pos + 1j - 1 not in visited:
                pos += 1j - 1
            elif pos + 1j + 1 not in visited:
                pos += 1 + 1j
            else:
                visited.add(pos)
                sand_units += 1
                break


def drop_sand_until_stability(
    rocks: set[complex], floor: int, pouring_point: complex = 500
):
    """
    Simulate the falling sand until it is stable
    """
    sand_units = 0
    visited = set(rocks)
    y_max = floor - 1

    while pouring_point not in visited:
        pos = pouring_point

        while pos.imag < y_max:
            # Move the sand down or down-left or down-right
            if pos + 1j not in visited:
                pos += 1j
            elif pos + 1j - 1 not in visited:
                pos += 1j - 1
            elif pos + 1j + 1 not in visited:
                pos += 1 + 1j
            else:
                break
        visited.add(pos)
        sand_units += 1
    
    return sand_units


def main(filepath):
    paths = list(read_inputs(filepath))
    rocks, y_max = parse_inputs(paths)
    print("Part 1:", drop_sand_until_abyss(rocks, y_max))
    print("Part 2:", drop_sand_until_stability(rocks, y_max + 2))
