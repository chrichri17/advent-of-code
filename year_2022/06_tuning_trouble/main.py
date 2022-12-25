def find_marker(filename, len_sequence=4):
    stream = open(filename).read().strip()

    for i in range(len_sequence, len(stream)):
        if len(set(stream[i - len_sequence : i])) == len_sequence:
            return i


def main(filename):
    print("Part 1:", find_marker(filename))
    print("Part 2:", find_marker(filename, 14))
