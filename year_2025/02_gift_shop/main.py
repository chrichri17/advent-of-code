# https://adventofcode.com/2025/day/2

Range = tuple[int, ...]


def read_inputs(filepath) -> list[Range]:
    with open(filepath) as file:
        return [
            tuple(map(int, r.split("-"))) for r in file.readline().strip().split(",")
        ]


def solve(ranges: list[Range], is_valid):
    total = 0
    for start, end in ranges:
        total += sum(pid for pid in range(start, end + 1) if is_valid(pid))
    return total


def is_repeated_twice(pid):
    sid = str(pid)
    length = len(sid)
    if length % 2 == 1:
        return False
    mid = length // 2
    return sid[:mid] == sid[mid:]


def is_repeated_any(pid):
    sid = str(pid)
    length = len(sid)

    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len != 0:
            continue
        pattern = sid[:pattern_len]
        if sid == pattern * (length // pattern_len):
            return True
    return False


def main(filepath):
    ranges = read_inputs(filepath)

    print("Part 1:", solve(ranges, is_valid=is_repeated_twice))
    print("Part 2:", solve(ranges, is_valid=is_repeated_any))
