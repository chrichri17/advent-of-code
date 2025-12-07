# https://adventofcode.com/2025/day/6

from dataclasses import dataclass
from math import prod
from typing import Literal, cast

Operator = Literal["+", "*"]

OPERATIONS = {
    "+": sum,
    "*": prod,
}


@dataclass
class Problem:
    operator: Operator
    numbers: list[str]

    @property
    def operation(self):
        return OPERATIONS[self.operator]

    def solve(self, method="default"):
        return self.operation(self._get_ints(method))

    def _get_ints(self, method="default"):
        if method == "default":
            return map(int, self.numbers)
        elif method == "cephalopod":
            M = max(map(len, self.numbers))
            nums = [
                "".join(num[j] for num in self.numbers if j < len(num))
                for j in range(M)
            ]
            return map(int, nums)
        else:
            raise ValueError(f"Unknown method: {method}")


def read_inputs(filepath):
    with open(filepath) as file:
        lines = [line[:-1] for line in file.readlines()]  # strip newline
        opstr = lines.pop()

        op_indexes = [i for i, char in enumerate(opstr) if char in "+*"]
        operations: list[Operator] = [cast(Operator, op) for op in opstr.split()]

        max_line_length = max(len(line) for line in lines)

        problems: list[Problem] = []
        for i, (start, end) in enumerate(
            zip(op_indexes, op_indexes[1:] + [max_line_length])
        ):
            # strip column separator
            if end != max_line_length:
                end -= 1
            problems.append(
                Problem(
                    operator=operations[i],
                    numbers=[line[start:end] for line in lines],
                )
            )

        return problems


def solve(problems, method="default"):
    return sum(problem.solve(method) for problem in problems)


def main(filepath):
    problems = read_inputs(filepath)
    print("Part 1:", solve(problems))
    print("Part 2:", solve(problems, method="cephalopod"))
