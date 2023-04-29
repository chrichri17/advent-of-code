from typing import Generator

PacketData = int | list["PacketData"]

Packet = list[PacketData]

Pair = tuple[Packet, Packet]


def get_packets_pairs(filename) -> Generator[Pair, None, None]:
    with open(filename) as file:
        for pair in file.read().strip().split("\n\n"):
            yield tuple(map(eval, pair.split("\n")))


def compare(left: PacketData, right: PacketData) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            res = compare(l, r)
            if res is not None:
                return res
        p, q = len(left), len(right)
        return None if p == q else p < q

    if isinstance(left, int):
        return compare([left], right)
    else:
        return compare(left, [right])


def get_ordered_pairs(pairs: list[Pair]) -> Generator[int, None, None]:
    for i, (left, right) in enumerate(pairs, start=1):
        if compare(left, right) == True:
            yield i


def get_decoder_key(pairs: list[Pair]) -> int:
    # Positions of the dividers after sorting
    # NB: we don't really need to sort, since only
    # the positions after the sorting are required
    i0, j0 = 1, 2
    packets = (packet for pair in pairs for packet in pair)

    for packet in packets:
        if compare(packet, [[2]]) == True:
            i0 += 1
            j0 += 1
        elif compare(packet, [[6]]) == True:
            j0 += 1

    return i0 * j0


def main(filename):
    pairs = list(get_packets_pairs(filename))
    print("Part 1:", sum(get_ordered_pairs(pairs)))
    print("Part 2:", get_decoder_key(pairs))
