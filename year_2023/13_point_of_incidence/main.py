def read_inputs(filepath):
    with open(filepath) as file:
        patterns = file.read().split("\n\n")
        for pattern in patterns:
            yield pattern.splitlines()


def find_reflection_lines(pattern, smudge_count=0):
    n, m = len(pattern), len(pattern[0])
    for r in range(n - 1):
        invalids = 0

        for pad in range(n):
            left = r - pad
            right = r + 1 + pad

            if left >= 0 and right < n:
                for c in range(m):
                    if pattern[left][c] != pattern[right][c]:
                        invalids += 1
                        if invalids > smudge_count:
                            break
        if invalids == smudge_count:
            yield r + 1


def solve(filepath, smudge_count=0):
    total = 0
    for pattern in read_inputs(filepath):
        r = sum(find_reflection_lines(pattern, smudge_count))
        c = sum(find_reflection_lines(list(zip(*pattern)), smudge_count))
        total += 100 * r + c
    return total


def main(filepath):
    print("Part 1:", solve(filepath))
    print("Part 2:", solve(filepath, 1))
