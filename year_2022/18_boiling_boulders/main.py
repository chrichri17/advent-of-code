from collections import deque
from typing import Generator

Cube = tuple[int, int, int]


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield tuple(map(int, line.strip().split(",")))


dirs = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0)]


def get_neighbors(cube: Cube) -> Generator[Cube, None, None]:
    x, y, z = cube
    for dx, dy, dz in dirs:
        yield (x + dx, y + dy, z + dz)


def surface_area(cubes: set[Cube]) -> int:
    count = 0

    for cube in cubes:
        for neighbor in get_neighbors(cube):
            # Check if the cubes are adjacents
            if neighbor not in cubes:
                count += 1

    return count


def exterior_surface_area(cubes: set[Cube]) -> int:
    # Get minimum and maximum in each direction
    mx = my = mz = float("inf")
    Mx = My = Mz = 0

    for x, y, z in cubes:
        mx, Mx = min(mx, x), max(Mx, x)
        my, My = min(my, y), max(My, y)
        mz, Mz = min(mz, z), max(Mz, z)

    # Expand the exterior
    mx, Mx = mx - 1, Mx + 1
    my, My = my - 1, My + 1
    mz, Mz = mz - 1, Mz + 1

    # Apply a DFS algorithm to find cubes that are part of
    # the exterior within the given bounds (mx, my, mz) (Mx, My, Mz)
    def in_bound(cube: Cube) -> bool:
        mins = (mx, my, mz)
        maxs = (Mx, My, Mz)
        return all(mins[i] <= cube[i] <= maxs[i] for i in range(3))

    stack = [(mx, my, mz)]
    exterior = set()

    while stack:
        cube = stack.pop()
        if cube in exterior or cube in cubes or not in_bound(cube):
            continue

        exterior.add(cube)
        for neighbor in get_neighbors(cube):
            stack.append(neighbor)

    # Do the counting
    count = 0

    for cube in cubes:
        for neighbor in get_neighbors(cube):
            if neighbor in exterior:
                count += 1

    return count


def main(filepath):
    cubes = set(read_inputs(filepath))
    print("Part 1:", surface_area(cubes))
    print("Part 2:", exterior_surface_area(cubes))
