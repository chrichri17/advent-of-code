# https://adventofcode.com/2024/day/3
import re


def read_inputs(filepath):
    with open(filepath) as file:
        return file.read().strip()


pattern = re.compile(r"mul\((\d+),(\d+)\)")


def part1(filepath):
    return sum(int(x) * int(y) for x, y in pattern.findall(read_inputs(filepath)))


def part2(filepath):
    memory = read_inputs(filepath)
    groups = re.split("do\(\)|don't\(\)", memory)
    enabled = [True] + [
        instruction == "do()" for instruction in re.findall("do\(\)|don't\(\)", memory)
    ]
    return sum(
        int(x) * int(y)
        for enable, group in zip(enabled, groups)
        if enable
        for x, y in pattern.findall(group)
    )


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
