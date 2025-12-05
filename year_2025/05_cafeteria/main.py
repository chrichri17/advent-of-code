# https://adventofcode.com/2025/day/5


def read_inputs(filepath):
    with open(filepath) as file:
        ranges, ingredients = file.read().split("\n\n")
        ranges = [tuple(map(int, line.split("-"))) for line in ranges.strip().split()]
        ingredients = list(map(int, ingredients.strip().split()))
        return ranges, ingredients


def part1(filepath):
    ranges, ingredients = read_inputs(filepath)
    return sum(
        any(lo <= ingredient <= hi for lo, hi in ranges) for ingredient in ingredients
    )


# Easier to reason about
def part2(filepath):
    ranges, _ = read_inputs(filepath)
    ranges.sort()  # This ensures we always have the smallest range start in our loop

    interval = ranges[0]
    count = interval[1] - interval[0] + 1

    for lo, hi in ranges:
        curr_lo, curr_hi = interval
        # No overlap: curr_lo, curr_hi, lo, hi
        if curr_hi < lo:
            count += hi - lo + 1
            interval = (lo, hi)
        # Overlap and not superset: curr_lo, lo, curr_hi, hi
        elif curr_hi <= hi:
            count += hi - curr_hi
            interval = (curr_lo, hi)
        # Overlap with superset: curr_lo, lo, hi, curr_hi
        else:
            pass
        # Since we always have the smallest range start, we can't have lo < curr_lo

    return count


# My first over complicated solution
def part2_without_sort(filepath):
    from collections import deque

    ranges, _ = read_inputs(filepath)
    unique_ranges = []

    queue = deque(ranges[::-1])

    while queue:
        lo, hi = queue.pop()

        overlaps = False  # at least one overlap

        for curr_lo, curr_hi in unique_ranges:
            if hi < curr_lo or curr_hi < lo:
                continue

            overlaps = True

            if curr_lo <= lo:
                # curr_lo, lo, curr_hi, hi
                if hi > curr_hi:
                    queue.append((curr_hi + 1, hi))
                # curr_lo, lo, hi, curr_hi
                else:
                    pass
            else:
                # lo, curr_lo, curr_hi
                queue.append((lo, curr_lo - 1))
                # lo, curr_lo, curr_hi, hi
                if hi > curr_hi:
                    queue.append((curr_hi + 1, hi))

        if not overlaps:
            unique_ranges.append((lo, hi))

    return sum(hi - lo + 1 for lo, hi in unique_ranges)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
    assert part2_without_sort(filepath) == part2(filepath)
