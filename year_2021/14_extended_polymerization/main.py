# https://adventofcode.com/2021/day/14

from collections import Counter


def read_inputs(filepath):
    with open(filepath) as file:
        polymer, _, *rules = file.read().splitlines()
        rules = {rule[:2]: rule[-1:] for rule in rules}
        return polymer, rules


def process(polymer, rules, times=10):
    pairs = Counter([a + b for a, b in zip(polymer, polymer[1:])])
    counter = Counter(polymer)
    for _ in range(times):
        new_pairs = Counter()
        for pair, count in pairs.items():
            if pair in rules:
                a, c = pair
                b = rules[pair]
                new_pairs[a + b] += count
                new_pairs[b + c] += count
                counter[b] += count
            else:
                new_pairs[pair] += count
        pairs = new_pairs
    a, *_, b = counter.most_common()
    return a[1] - b[1]


def main(filepath):
    polymer, rules = read_inputs(filepath)
    print("Part 1:", process(polymer, rules))
    print("Part 2:", process(polymer, rules, 40))
