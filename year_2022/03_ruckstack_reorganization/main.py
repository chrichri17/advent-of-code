from string import ascii_letters

PRIORITY = {s: i + 1 for i, s in enumerate(ascii_letters)}


def part1(filepath):
    priorities_sum = 0

    with open(filepath) as file:
        for line in file.readlines():
            mid = len(line) // 2
            uniques = set(line[:mid]).intersection(line[mid:])
            if len(uniques) != 1:
                # this shouldn't happen
                raise ValueError()
            shared = uniques.pop()
            priorities_sum += PRIORITY[shared]

    return priorities_sum


def part2(filepath):
    priorities_sum = 0

    with open(filepath) as file:
        lines = file.readlines()

        for i in range(len(lines) // 3):
            uniques = (
                set(lines[3 * i].strip())
                .intersection(lines[3 * i + 1].strip())
                .intersection(lines[3 * i + 2].strip())
            )
            if len(uniques) != 1:
                # this shouldn't happen
                raise ValueError()
            shared = uniques.pop()
            priorities_sum += PRIORITY[shared]

    return priorities_sum


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
