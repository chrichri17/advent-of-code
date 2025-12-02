# https://adventofcode.com/2025/day/1


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield (-1 if line[0] == "L" else 1, int(line[1:]))


def rotate(pos: int, direction: int, times: int):
    # We could also compute crosses like this:
    # if direction == 1:  # Moving right
    #     # How many times do we cross 0 going from pos to pos+times?
    #     crosses = (pos + times) // 100
    # else:  # Moving left
    #     # How many times do we cross 0 going from pos to pos-times?
    #     crosses = (pos - 1) // 100 - (pos - times - 1) // 100
    crosses = 0
    for _ in range(times):
        pos = (pos + direction) % 100
        if pos == 0:
            crosses += 1
    return pos, crosses


def part1(filepath):
    pos = 50
    count = 0
    for d, times in read_inputs(filepath):
        pos, _ = rotate(pos, d, times)
        if pos == 0:
            count += 1
    return count


def part2(filepath):
    pos = 50
    count = 0
    for d, times in read_inputs(filepath):
        pos, crosses = rotate(pos, d, times)
        count += crosses
    return count


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
