def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield map(int, line.strip().replace(",", "-").split("-"))


def part1(filepath):
    nb_inclusions = 0

    for a, b, x, y in read_inputs(filepath):
        if (a <= x and y <= b) or (x <= a and b <= y):
            nb_inclusions += 1

    return nb_inclusions


def part2(filepath):
    nb_overlap = 0

    for a, b, x, y in read_inputs(filepath):
        # Not optimal but simple and fast enough
        if set(range(a, b + 1)) & set(range(x, y + 1)):
            nb_overlap += 1

    return nb_overlap


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
