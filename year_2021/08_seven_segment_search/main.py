# https://adventofcode.com/2021/day/08

from collections import Counter

displays = "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg".split()
digit_to_display = {k: v for k, v in enumerate(displays)}
display_to_digit = {v: k for k, v in enumerate(displays)}


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            patterns, output = line.strip().split(" | ")
            yield patterns.strip().split(), output.strip().split()


def part1(filepath):
    total = 0
    for _, output in read_inputs(filepath):
        total += sum(1 for digit in output if len(digit) in {2, 3, 4, 7})
    return total


def guess_pattern_mapping(patterns: list[str]) -> dict[str, str]:
    counter = Counter("".join(patterns))
    # Counting the number of time a char appears in the patterns will help guess the mapping
    # Counter(displays) = Counter({'f': 9, 'a': 8, 'c': 8, 'g': 7, 'd': 7, 'b': 6, 'e': 4})
    f = next(k for k, v in counter.items() if v == 9)
    b = next(k for k, v in counter.items() if v == 6)
    e = next(k for k, v in counter.items() if v == 4)

    one = next(d for d in patterns if len(d) == 2)
    four = next(d for d in patterns if len(d) == 4)

    # Given that one is "cf", {c} = set(one) - {f}
    diff = set(one) - {f}
    assert len(diff) == 1
    c = diff.pop()

    # Now we know a since a and c are the only characters that appear 8 times
    a = next(k for k, v in counter.items() if v == 8 and k != c)

    # Given that four is "bcdf", we know that {d} = set(four) - {b, c, f}
    diff = set(four) - {b, c, f}
    assert len(diff) == 1
    d = diff.pop()

    # Now we know g since g and d are the only characters that appear 7 times
    g = next(k for k, v in counter.items() if v == 7 and k != d)

    return {a: "a", b: "b", c: "c", d: "d", e: "e", f: "f", g: "g"}


def part2(filepath):
    total = 0
    for patterns, output in read_inputs(filepath):
        mapping = guess_pattern_mapping(patterns)
        total += int(
            "".join(
                str(display_to_digit["".join(sorted(mapping[k] for k in digit))])
                for digit in output
            )
        )
    return total


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
