# https://adventofcode.com/2015/day/3


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            return list(line.strip())


DIRECTIONS = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


def part1(filepath):
    moves = read_inputs(filepath)
    houses = {(0, 0)}
    x, y = (0, 0)
    for move in moves:
        dx, dy = DIRECTIONS[move]
        x, y = x + dx, y + dy
        houses.add((x, y))
    return len(houses)


def part2(filepath):
    moves = read_inputs(filepath)
    houses = {(0, 0)}
    x1, y1 = (0, 0)
    x2, y2 = (0, 0)
    for i, move in enumerate(moves):
        dx, dy = DIRECTIONS[move]
        if i % 2 == 0:
            x1, y1 = x1 + dx, y1 + dy
            houses.add((x1, y1))
        else:
            x2, y2 = x2 + dx, y2 + dy
            houses.add((x2, y2))
    return len(houses)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
