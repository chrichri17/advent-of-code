import numpy as np


def parse_inputs(filepath):
    heightmap = []
    with open(filepath) as file:
        for line in file.readlines():
            heightmap.append(list(map(int, list(line.strip()))))
    return heightmap


def part1(filepath):
    tree_map = np.array(parse_inputs(filepath))
    n, m = tree_map.shape
    nb_visible = 2 * (n + m - 2)

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            left = max(tree_map[i, :j])
            right = max(tree_map[i, j + 1 :])
            up = max(tree_map[:i, j])
            bottom = max(tree_map[i + 1 :, j])

            if tree_map[i, j] > min(left, right, up, bottom):
                nb_visible += 1

    return nb_visible


def part2(filepath):
    tree_map = np.array(parse_inputs(filepath))
    n, m = tree_map.shape
    max_scenic_score = 0

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            left = 0
            for k in range(j - 1, -1, -1):
                left += 1
                if tree_map[i, k] >= tree_map[i, j]:
                    break

            right = 0
            for k in range(j + 1, m):
                right += 1
                if tree_map[i, k] >= tree_map[i, j]:
                    break

            up = 0
            for k in range(i - 1, -1, -1):
                up += 1
                if tree_map[k, j] >= tree_map[i, j]:
                    break

            bottom = 0
            for k in range(i + 1, n):
                bottom += 1
                if tree_map[k, j] >= tree_map[i, j]:
                    break

            max_scenic_score = max(max_scenic_score, left * right * up * bottom)

    return max_scenic_score


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
