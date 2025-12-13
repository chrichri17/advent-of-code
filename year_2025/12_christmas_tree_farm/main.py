# https://adventofcode.com/2025/day/12

# This is based on the inputs specificities
# See https://www.reddit.com/r/adventofcode/comments/1pkje0o/2025_day_12_solutions/
# # And check brte_force.py for the real solution with backtracking
def solve(filepath):
    with open(filepath) as file:
        data = file.read()
        *shapes, regions = data.strip().split("\n\n")

        areas = {}

        for shape in shapes:
            lines = shape.splitlines()
            sid = int(lines.pop(0)[:-1])
            area = sum(row.count("#") for row in lines)
            areas[sid] = area

    total = 0
    for region in regions.splitlines():
        size, _, counts = region.partition(": ")
        W, H = map(int, size.split("x"))
        counts = tuple(map(int, counts.split()))

        grid_size = W * H
        total_area = sum(areas[i] * count for i, count in enumerate(counts))
        # 1.1, 1.2 and 1.3 works
        if total_area * 1.3 < grid_size:
            total += 1

    return total


def main(filepath):
    if "in" in filepath.name:
        print("Part 1:", solve(filepath))
