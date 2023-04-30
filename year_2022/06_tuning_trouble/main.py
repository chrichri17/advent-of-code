def find_marker(filepath, len_sequence=4):
    stream = open(filepath).read().strip()

    for i in range(len_sequence, len(stream)):
        if len(set(stream[i - len_sequence : i])) == len_sequence:
            return i


def main(filepath):
    print("Part 1:", find_marker(filepath))
    print("Part 2:", find_marker(filepath, 14))
