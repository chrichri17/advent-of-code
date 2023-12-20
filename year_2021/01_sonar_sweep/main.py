# https://adventofcode.com/2021/day/1


def read_inputs(filepath):
    with open(filepath) as file:
        return list(map(int, file.read().splitlines()))


def count_increase(nums: list[int], sliding_window=1):
    count = 0
    last = None
    for i in range(sliding_window, len(nums) + 1):
        s = sum(nums[i - sliding_window : i])
        if last is not None and last < s:
            count += 1
        last = s
    return count


def main(filepath):
    nums = read_inputs(filepath)
    print("Part 1:", count_increase(nums))
    print("Part 2:", count_increase(nums, 3))
