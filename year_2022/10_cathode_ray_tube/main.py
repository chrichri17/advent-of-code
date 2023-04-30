CYCLES = {20, 60, 100, 140, 180, 220}


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip().split()


def part1(filepath):
    x = 1
    cycle = 0
    signal_strength_sum = 0

    def incr_cycle():
        nonlocal x, cycle, signal_strength_sum
        cycle += 1
        if cycle in CYCLES:
            signal_strength_sum += x * cycle

    for instruction in read_inputs(filepath):
        incr_cycle()

        if len(instruction) == 2:
            incr_cycle()
            x += int(instruction[-1])

    return signal_strength_sum


def part2(filepath):
    x = 1
    cycle = 0
    crt = [["  " for _ in range(40)] for _ in range(6)]

    def incr_cycle():
        nonlocal x, cycle, crt
        p, q = divmod(cycle, 40)
        cycle += 1
        if x % 40 <= cycle % 40 < x % 40 + 3:
            crt[p][q] = "##"

    for instruction in read_inputs(filepath):
        incr_cycle()

        if len(instruction) == 2:
            incr_cycle()
            x += int(instruction[-1])

    return "\n".join(map("".join, crt))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath), sep="\n")
