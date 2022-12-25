import re
from collections import deque, defaultdict


def read_inputs(filename):
    stacks = defaultdict(deque)

    with open(filename) as file:
        while True:
            line = file.readline().rstrip()
            if line[-1].isdigit():
                break

            for j in range(1, len(line), 4):
                if line[j] != " ":
                    stacks[j // 4].appendleft(line[j])

        yield [stacks[idx] for idx in sorted(stacks.keys())]

        # New line before instructions
        file.readline()

        # Read instructions
        pattern = "move (\d+) from (\d+) to (\d+)"
        for instruction in file.readlines():
            match = re.search(pattern, instruction.rstrip())
            amount, i, j = map(int, match.groups())
            i -= 1
            j -= 1
            yield amount, i, j


def crate_mover(filename, version=9000):
    if version not in {9000, 9001}:
        raise ValueError(f"unknown version {version}")

    inputs = read_inputs(filename)
    stacks = next(inputs)

    for amount, i, j in inputs:
        source = stacks[i]
        target = stacks[j]

        insert_pos = len(target)

        for _ in range(amount):
            if len(source) == 0:
                # This shouldn't happen
                raise ValueError()

            item = source.pop()
            if version == 9000:
                target.append(item)
            else:
                target.insert(insert_pos, item)

    # Return top values
    tops = [stack[-1] if stack else "#" for stack in stacks]
    return "".join(tops)


def main(filename):
    print("Part 1:", crate_mover(filename, version=9000))
    print("Part 2:", crate_mover(filename, version=9001))
