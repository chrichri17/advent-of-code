# https://adventofcode.com/2024/day/25


def read_inputs(filepath):
    with open(filepath) as file:
        grids = file.read().strip().split("\n\n")
        keys = set()
        locks = set()

        for grid_raw in grids:
            grid = grid_raw.strip().split("\n")
            nrows, ncols = len(grid), len(grid[0])
            is_lock = False
            if all(grid[0][i] == "#" for i in range(ncols)):
                is_lock = True

            heights = [-1] * ncols
            for r in range(nrows):
                for c in range(ncols):
                    if grid[r][c] == "#":
                        heights[c] += 1

            if is_lock:
                locks.add(tuple(heights))
            else:
                keys.add(tuple(heights))

        return nrows, ncols, keys, locks


def part1(filepath):
    nrows, ncols, keys, locks = read_inputs(filepath)
    count = 0
    for key in keys:
        for lock in locks:
            if all(key[i] + lock[i] < nrows - 1 for i in range(ncols)):
                count += 1
    return count


def part2(filepath):
    return "🎉🎉🎉 Year 2024 done 🎉🎉🎉"


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
