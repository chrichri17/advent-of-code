CYCLES = {20, 60, 100, 140, 180, 220}


def read_inputs(filename):
    with open(filename) as file:
        for line in file.readlines():
            yield line.strip().split()


def part1(filename):
    x = 1
    cycle = 0
    signal_strength_sum = 0

    def incr_cycle():
        nonlocal x, cycle, signal_strength_sum
        cycle += 1
        if cycle in CYCLES:
            signal_strength_sum += x * cycle

    for instruction in read_inputs(filename):
        incr_cycle()

        if len(instruction) == 2:
            incr_cycle()
            x += int(instruction[-1])

    return signal_strength_sum


def part2(filename):
    x = 1
    cycle = 0
    crt = [["  " for _ in range(40)] for _ in range(6)]

    def incr_cycle():
        nonlocal x, cycle, crt
        p, q = divmod(cycle, 40)
        cycle += 1
        if x % 40 <= cycle % 40 < x % 40 + 3:
            crt[p][q] = "##"

    for instruction in read_inputs(filename):
        incr_cycle()

        if len(instruction) == 2:
            incr_cycle()
            x += int(instruction[-1])

    return "\n".join(map(lambda row: "".join(row), crt))


def main(filename):
    print("Part 1:", part1(filename))
    print("Part 2:", part2(filename), sep="\n")
