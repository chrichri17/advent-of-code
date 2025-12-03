# https://adventofcode.com/2025/day/3


def read_inputs(filepath):
    with open(filepath) as file:
        return [list(map(int, line.strip())) for line in file.readlines()]


def find_largest(nums, start=0, remaining=2, acc=""):
    if remaining == 0:
        return int(acc)

    end = len(nums) - remaining + 1
    pos, curr_max = start, -1

    for i in range(start, end):
        if nums[i] > curr_max:
            pos, curr_max = i, nums[i]

    return find_largest(nums, pos + 1, remaining - 1, acc + str(curr_max))


def solve(banks, ndigits=2):
    return sum(find_largest(bank, remaining=ndigits) for bank in banks)


def main(filepath):
    banks = read_inputs(filepath)
    print("Part 1:", solve(banks))
    print("Part 2:", solve(banks, ndigits=12))
