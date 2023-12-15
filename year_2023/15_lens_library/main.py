# https://adventofcode.com/2023/day/15

from collections import defaultdict


def read_inputs(filepath):
    with open(filepath) as file:
        return file.readline().strip().split(",")


def find(box, label):
    try:
        return box.index(label)
    except ValueError:
        return -1


def get_hash(data):
    current_value = 0

    for char in data:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


def part1(filepath):
    steps = read_inputs(filepath)
    return sum(get_hash(step) for step in steps)


def part2(filepath):
    steps = read_inputs(filepath)
    boxes = defaultdict(list)

    for step in steps:
        sep = "-" if step.endswith("-") else "="
        label, sep, focal_len = step.partition(sep)

        box = boxes[get_hash(label)]

        idx = find(list(map(lambda x: x[0], box)), label)
        if sep == "-" and idx != -1:
            box.pop(idx)
        elif sep == "=":
            if idx != -1:
                box[idx] = (label, focal_len)
            else:
                box.append((label, focal_len))

    total = 0
    for box_idx, box in boxes.items():
        for i, (label, focal_len) in enumerate(box, 1):
            total += (1 + box_idx) * i * int(focal_len)
    return total


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
