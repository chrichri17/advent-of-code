# https://adventofcode.com/2021/day/3


def read_inputs(filepath) -> list[list[int]]:
    with open(filepath) as file:
        return list(map(list, file.read().splitlines()))


def part1(filepath):
    bits = read_inputs(filepath)
    cols = list(map(list, zip(*bits)))
    gamma = "".join([max(col, key=col.count) for col in cols])
    epsilon = "".join([min(col, key=col.count) for col in cols])
    return int(gamma, 2) * int(epsilon, 2)


def part2(filepath):
    bits = read_inputs(filepath)

    def deep_filter(bits, criteria, pos=0) -> str:
        col = [row[pos] for row in bits]
        bit = criteria(col, key=lambda x: (col.count(x), x))
        bits = [row for row in bits if row[pos] == bit]
        if len(bits) == 1:
            return int("".join(bits[0]), 2)
        return deep_filter(bits, criteria, pos + 1)

    oxygen = deep_filter(bits, max)
    co2 = deep_filter(bits, min)
    return oxygen * co2


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
