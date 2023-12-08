# https://adventofcode.com/2023/day/8

from itertools import cycle
from math import lcm


def read_inputs(filepath):
    with open(filepath) as file:
        insructions = [0 if i == "L" else 1 for i in file.readline().strip()]

        file.readline()

        network = {}
        for line in file.readlines():
            node, children = line.strip().split(" = ")
            network[node] = children[1:-1].split(", ")

        return insructions, network


def part1(filepath):
    instructions, network = read_inputs(filepath)
    instructions = cycle(instructions)

    steps = 0
    curr = "AAA"

    while curr != "ZZZ":
        curr = network[curr][next(instructions)]
        steps += 1

    return steps


def part2(filepath):
    instructions, network = read_inputs(filepath)

    starts = [node for node in network if node.endswith("A")]

    cycles = []
    for start in starts:
        it = cycle(instructions)
        curr = start
        steps = 0

        while not curr.endswith("Z"):
            curr = network[curr][next(it)]
            steps += 1
        cycles.append(steps)

    return lcm(*cycles)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
