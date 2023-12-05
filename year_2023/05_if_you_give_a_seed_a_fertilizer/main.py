# https://adventofcode.com/2023/day/5


def read_inputs(filepath):
    blocks = []

    with open(filepath) as file:
        seeds, *groups = file.read().split("\n\n")
        seeds = list(map(int, seeds.split(":")[1].split()))
        for group in groups:
            ranges = []
            for r in group.splitlines()[1:]:
                ranges.append(tuple(map(int, r.split())))
            blocks.append(ranges)

    return seeds, blocks


def get_destination_number(block, seed) -> int:
    for a, b, c in block:
        if b <= seed <= b + c:
            return a + seed - b
    return seed


def split_interval(
    seed_range: tuple[int, int], block: [tuple[int, int, int]]
) -> list[tuple[int, int]]:
    # This function assume block is sorted by x -> x[1]
    start, end = seed_range

    # Exit if largest range in block is smaller than seed_range
    if start > block[-1][1] + block[-1][2]:
        return [seed_range]
    # Exit if smallest range in block is larger than seed_range
    if end < block[0][1]:
        return [seed_range]

    intervals = []
    for a, b, c in block:
        overlap_start, overlap_end = max(start, b), min(end, b + c)
        if overlap_start < overlap_end:
            if overlap_start > start:
                # Add the source interval as is.
                intervals.append((start, overlap_start))
            # Map the source interval to the destination interval
            intervals.append((overlap_start - b + a, overlap_end - b + a))
            start = overlap_end

    return intervals


# Part 1
def min_location_number(filepath) -> int:
    seeds, blocks = read_inputs(filepath)

    for block in blocks:
        for i, seed in enumerate(seeds):
            seeds[i] = get_destination_number(block, seed)

    return min(seeds)


# Part 2
def min_location_number_from_ranges(filepath) -> int:
    sr, blocks = read_inputs(filepath)
    seeds = []
    for i in range(0, len(sr), 2):
        seeds.append((sr[i], sr[i] + sr[i + 1]))

    for block in blocks:
        block.sort(key=lambda x: x[1])

        new_seeds = []
        for seed in seeds:
            new_seeds.extend(split_interval(seed, block))
        seeds = new_seeds

    return min(seeds)[0]


def main(filepath):
    print("Part 1:", min_location_number(filepath))
    print("Part 2:", min_location_number_from_ranges(filepath))
