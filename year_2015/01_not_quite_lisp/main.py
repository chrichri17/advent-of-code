# https://adventofcode.com/2015/day/14


def read_inputs(filepath):
    with open(filepath) as file:
        return list(file.read().strip())


def walk(data):
    floor = 0
    basement = 0
    for i, x in enumerate(data, 1):
        floor += 1 if x == "(" else -1
        if floor == -1 and not basement:
            basement = i
    return basement, floor


def main(filepath):
    data = read_inputs(filepath)
    basement, floor = walk(data)
    print("Part 1:", floor)
    print("Part 2:", basement)
