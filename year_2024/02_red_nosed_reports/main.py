# https://adventofcode.com/2024/day/2


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.read().splitlines():
            yield list(map(int, line.strip().split()))


def safe(levels: list[int]) -> bool:
    diff = [x - y for x, y in zip(levels, levels[1:])]
    return all(1 <= d <= 3 for d in diff) or all(-3 <= d <= -1 for d in diff)


def part1(filepath):
    return sum(safe(levels) for levels in read_inputs(filepath))


def part2(filepath):
    count = 0
    for levels in read_inputs(filepath):
        count += safe(levels) or any(
            safe(levels[:i] + levels[i + 1 :]) for i in range(len(levels))
        )
    return count


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
