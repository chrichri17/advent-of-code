# https://adventofcode.com/2021/day/16

from math import prod
from types import SimpleNamespace


def consume(bits: str, n: int) -> tuple[int, str]:
    return int(bits[:n], base=2), bits[n:]


def consume_string(bits: str, n: int) -> tuple[str, str]:
    return bits[:n], bits[n:]


# For debugging

# def to_json(packet):
#     json_packet = vars(packet)
#     for key, value in json_packet.items():
#         if isinstance(value, SimpleNamespace):
#             json_packet[key] = to_json(value)
#         if isinstance(value, list):
#             json_packet[key] = [to_json(v) for v in value]
#         if isinstance(value, dict):
#             json_packet[key] = {k: to_json(v) for k, v in value.items()}
#     return json_packet


def decode(bits: str, packet: SimpleNamespace) -> str:
    bits_copy = bits[:]
    n = len(bits)

    packet.version, bits = consume(bits, 3)
    packet.pid, bits = consume(bits, 3)

    if packet.pid == 4:
        packet.kind = "literal"
        packet.value, bits = decode_literal(bits)
    else:
        packet.kind = "operator"
        packet.mode, packet.children, bits = decode_operator(bits)
        packet.value = get_operator_value(packet.pid, packet.children)

    packet.length = n - len(bits)
    packet.raw = bits_copy[: packet.length]

    return bits


def decode_literal(bits: str) -> tuple[int, str]:
    value = ""
    while True:
        group, bits = consume_string(bits, 5)
        value += group[1:]
        if group[0] == "0":
            break
    return int(value, 2), bits


def decode_operator(bits: str) -> tuple[int, list[SimpleNamespace], str]:
    mode, bits = consume(bits, 1)
    children = []
    if mode == 0:
        children_length, bits = consume(bits, 15)
        length = 0

        while length < children_length:
            subpacket = SimpleNamespace()
            bits = decode(bits, subpacket)
            children.append(subpacket)
            length += subpacket.length
    else:
        nb_children, bits = consume(bits, 11)

        for _ in range(nb_children):
            subpacket = SimpleNamespace()
            bits = decode(bits, subpacket)
            children.append(subpacket)
    return mode, children, bits


def get_operator_value(pid: int, children: list[SimpleNamespace]) -> int:
    if pid == 0:
        return sum(child.value for child in children)
    elif pid == 1:
        return prod(child.value for child in children)
    elif pid == 2:
        return min(child.value for child in children)
    elif pid == 3:
        return max(child.value for child in children)
    elif pid == 5:
        assert len(children) == 2
        a, b = children
        return int(a.value > b.value)
    elif pid == 6:
        assert len(children) == 2
        a, b = children
        return int(a.value < b.value)
    elif pid == 7:
        assert len(children) == 2
        a, b = children
        return int(a.value == b.value)


def read_inputs(filepath):
    with open(filepath) as f:
        return "".join(bin(int(c, base=16))[2:].zfill(4) for c in f.read().strip())


def get_vsum(packet: SimpleNamespace):
    if packet.kind == "literal":
        return packet.version
    return packet.version + sum(get_vsum(child) for child in packet.children)


def main(filepath):
    bits = read_inputs(filepath)
    packet = SimpleNamespace()
    decode(bits, packet)
    print("Part 1:", get_vsum(packet))
    print("Part 2:", packet.value)
