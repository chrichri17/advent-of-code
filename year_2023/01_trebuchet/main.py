# https://adventofcode.com/2023/day/1

import re

SPELLED_NUMBERS = r"one|two|three|four|five|six|seven|eight|nine"

store = {k: str(v) for v, k in enumerate(SPELLED_NUMBERS.split("|"), 1)}
store.update({k[::-1]: v for k, v in store.items()})


def lookup(key: str) -> str:
    return store.get(key, key)


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


def get_calibration_value(
    line: str,
    lp: re.Pattern,
    rp: re.Pattern,
) -> int:
    first = lookup(lp.search(line).group(0))
    last = lookup(rp.search(line[::-1]).group(0))
    return int(first + last)


def part1(filepath):
    pattern = re.compile(r"\d")  # search for digits
    return sum(
        get_calibration_value(line, pattern, pattern) for line in read_inputs(filepath)
    )


def part2(filepath):
    # search for digits or spelled numbers forwards
    lp = re.compile(r"\d|" + SPELLED_NUMBERS)
    # search for digits or spelled numbers backwards
    rp = re.compile(r"\d|" + SPELLED_NUMBERS[::-1])
    return sum(get_calibration_value(line, lp, rp) for line in read_inputs(filepath))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
