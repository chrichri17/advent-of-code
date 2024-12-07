# https://adventofcode.com/2024/day/07
from itertools import product


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            expected, nums = line.strip().split(": ")
            yield int(expected), list(map(int, nums.split()))


EVALUATORS = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
    "||": lambda a, b: int(str(a) + str(b)),
}


# This is slow for part 2
# The recursive approach is a faster solution
def total_calibration(equations, operations=["+", "*"]):
    total = 0
    for expected, nums in equations:
        for ops in product(operations, repeat=len(nums) - 1):
            if evaluate(nums, ops) == expected:
                total += expected
                break
    return total


def evaluate(nums: list[int], ops: list[str]) -> int:
    val = nums[0]
    for i, op in enumerate(ops):
        evaluator = EVALUATORS[op]
        val = evaluator(val, nums[i + 1])
    return val


# Recursive approach
# Faster than the previous solution, but still slow (~4s for part 2)
def total_calibration_recursive(equations, operations=["+", "*"]):
    total = 0
    for expected, nums in equations:
        if validate_equation(expected, nums, operations):
            total += expected
    return total


def validate_equation(expected: int, nums: list[int], operations) -> bool:
    if len(nums) == 1:
        return nums[0] == expected

    for op in operations:
        evaluator = EVALUATORS[op]
        new_nums = [evaluator(nums[0], nums[1])] + nums[2:]
        if validate_equation(expected, new_nums, operations):
            return True


def main(filepath):
    equations = list(read_inputs(filepath))

    print("Part 1:", total_calibration(equations))
    # print("Part 2:", total_calibration(equations, operations=["+", "*", "||"]))
    print(
        "Part 2:", total_calibration_recursive(equations, operations=["+", "*", "||"])
    )
