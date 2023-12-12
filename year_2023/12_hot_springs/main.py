# https://adventofcode.com/2023/day/12


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            record, blocks = line.strip().split()
            yield record, list(map(int, blocks.split(",")))


def solve(
    record: str,  # the record of springs
    blocks: tuple[int],  # the record of springs
    cache: dict[tuple[int, int, int], int],  # cache to speed up
    ri: int,  # current position in record
    bi: int,  # current position in blocks
    count: int,  # current number of blocks
) -> int:
    key = (ri, bi, count)
    if key in cache:
        return cache[key]

    if ri == len(record):
        # we consumed everything
        if bi == len(blocks) and count == 0:
            return 1
        # we consumed all springs and we just finished a block
        elif bi == len(blocks) - 1 and count == blocks[bi]:
            return 1
        return 0

    result = 0
    ## Case 1: current spring is # (or we replace a ? with #)
    if record[ri] == "#" or record[ri] == "?":
        result += solve(record, blocks, cache, ri + 1, bi, count + 1)

    ## Case 2: current spring is . (or we replace a ? with .)
    if record[ri] == "." or record[ri] == "?":
        if count == 0:
            # We were not building a block anyway.
            #   Advance ri.
            result += solve(record, blocks, cache, ri + 1, bi, 0)
        elif bi < len(blocks) and count == blocks[bi]:
            # We were building a block and we just finished it.
            #   Advance ri and bi. And reset current block length.
            result += solve(record, blocks, cache, ri + 1, bi + 1, 0)
        else:
            # Do nothing in other cases.
            pass

    cache[key] = result
    return result


def part1(filepath):
    total = 0
    for record, blocks in read_inputs(filepath):
        total += solve(record, blocks, {}, 0, 0, 0)
    return total


def part2(filepath):
    total = 0
    for record, blocks in read_inputs(filepath):
        record = "?".join([record] * 5)
        blocks = blocks * 5
        total += solve(record, blocks, {}, 0, 0, 0)
    return total


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
