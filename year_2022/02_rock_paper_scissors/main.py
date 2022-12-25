def read_inputs(filename):
    with open(filename) as file:
        for line in file.readlines():
            x, y = line.strip().split()
            yield ord(x) - ord("A"), ord(y) - ord("X")


def part1(filename):
    score = 0
    for foe, me in read_inputs(filename):
        # Score of the selected shape
        score += me + 1

        # Round outcome
        if me == foe:
            score += 3
        elif (me - foe) % 3 == 1:
            score += 6

    return score


def part2(filename):
    score = 0
    for foe, outcome in read_inputs(filename):
        # Round outcome : 0 if we lose; 3 if it's a draw and 6 else
        score += 3 * outcome

        # Score of the selected shape
        #   outcome - 1 is the shift to apply. If outcome is "X", i.e 0,
        #   we need to lose, so we choose the shape right before foe.
        score += (foe + outcome - 1) % 3 + 1

    return score


def main(filename):
    print("Part 1:", part1(filename))
    print("Part 2:", part2(filename))
