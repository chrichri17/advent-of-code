# https://adventofcode.com/2015/day/04

from hashlib import md5


def read_inputs(filepath):
    with open(filepath) as file:
        return file.read().strip()


def solve(secret_key, prefix="00000"):
    num = 0

    def can_mine(n):
        return md5((secret_key + str(n)).encode()).hexdigest().startswith(prefix)

    while not can_mine(num):
        num += 1

    return num


def main(filepath):
    secret_key = read_inputs(filepath)
    print("Part 1:", solve(secret_key))
    print("Part 2:", solve(secret_key, prefix="000000"))
