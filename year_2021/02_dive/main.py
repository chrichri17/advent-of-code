# https://adventofcode.com/2021/day/2


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            direction, amount = line.strip().split()
            yield direction, int(amount)


def part1(filepath):
    x, y = 0, 0

    for direction, amount in read_inputs(filepath):
        if direction == "forward":
            x += amount
        elif direction == "up":
            y -= amount
        elif direction == "down":
            y += amount

    return x * y


def part2(filepath):
    x, y, aim = 0, 0, 0

    for direction, amount in read_inputs(filepath):
        if direction == "forward":
            x += amount
            y += aim * amount
        elif direction == "up":
            aim -= amount
        elif direction == "down":
            aim += amount

    return x * y


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
