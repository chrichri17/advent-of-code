from dataclasses import dataclass
from typing import Callable, List
from copy import deepcopy


Operation = Callable[[int], int]


@dataclass
class Monkey:
    i: int
    items: List[int]
    operation: Operation
    divisibility_factor: int
    target_true: int
    target_false: int
    items_inspected: int = 0

    def test(self, item: int) -> bool:
        return item % self.divisibility_factor == 0


def read_inputs(filename):
    with open(filename) as file:
        for monkey_params in file.read().split("\n\n"):
            lines = monkey_params.splitlines()

            # Parse monkey params
            i = int(lines[0][:-1].split()[-1])
            items = list(map(int, lines[1].split(": ")[1].split(", ")))
            operation = eval("lambda old:%s" % lines[2].split("=")[-1])
            divisibility_factor = int(lines[3].split()[-1])
            target_true = int(lines[4].split()[-1])
            target_false = int(lines[5].split()[-1])

            yield Monkey(
                i, items, operation, divisibility_factor, target_true, target_false
            )


def run_round(monkeys: List[Monkey], normalize_wl: Operation):
    for monkey in monkeys:
        nb_inspected = len(monkey.items)

        for item in monkey.items:
            wl = normalize_wl(monkey.operation(item))
            idx = monkey.target_true if monkey.test(wl) else monkey.target_false
            monkeys[idx].items.append(wl)

        monkey.items_inspected += nb_inspected
        monkey.items = []


def track_most_active(monkeys: List[Monkey], normalize_wl: Operation, nb_run: int = 20):
    for _ in range(nb_run):
        run_round(monkeys, normalize_wl)
    counts = [monkey.items_inspected for monkey in monkeys]
    counts.sort()
    return counts[-1] * counts[-2]


def main(filename):
    monkeys: list[Monkey] = list(read_inputs(filename))

    normalize_wl = lambda x: x // 3
    print("Part 1:", track_most_active(deepcopy(monkeys), normalize_wl, nb_run=20))

    # Since all the divisibility factors are primes,
    # we can use the gauss theorem
    mod = 1
    for monkey in monkeys:
        mod *= monkey.divisibility_factor

    normalize_wl = lambda x: x % mod
    print("Part 2:", track_most_active(monkeys, normalize_wl, nb_run=10000))
