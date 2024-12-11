# https://adventofcode.com/2024/day/09
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Block:
    bid: int
    pos: int
    size: int

    @property
    def free(self):
        return self.bid == -1


def read_inputs(filepath):
    with open(filepath) as file:
        blocks = []
        fid = pos = 0
        for i, d in enumerate(file.read().strip()):
            d = int(d)
            if i % 2 == 0:
                blocks.append(Block(fid, pos, d))
                fid += 1
            else:
                blocks.append(Block(-1, pos, d))
            pos += d
        return blocks


def swap(blocks: list[Block], i: int, j: int):
    blocks[i], blocks[j] = blocks[j], blocks[i]
    blocks[i].pos, blocks[j].pos = blocks[j].pos, blocks[i].pos


def checksum(blocks: Iterator[Block]) -> int:
    csum = 0
    for b in blocks:
        if b.free:
            continue
        for i in range(b.pos, b.pos + b.size):
            csum += i * b.bid
    return csum


def flatten(blocks: Iterator[Block]) -> list[Block]:
    new_blocks = []
    for b in blocks:
        new_blocks += [Block(b.bid, b.pos + i, 1) for i in range(b.size)]
    return new_blocks


def to_str(blocks):
    print(
        "".join(
            str(b.bid) if not b.free else "." for b in blocks for _ in range(b.size)
        )
    )


def part1(filepath):
    blocks = flatten(read_inputs(filepath))
    i, j = (0, len(blocks) - 1)

    while j - i > 1:
        if not blocks[j].free:
            while i < j and not blocks[i].free:
                i += 1
            if j - i > 1:
                swap(blocks, i, j)
        j -= 1

    return checksum(blocks)


# Faster than solution in draft.py
def part2(filepath):
    blocks = read_inputs(filepath)
    files = {b.bid: (b.pos, b.size) for b in blocks if not b.free}
    blanks = [(b.pos, b.size) for b in blocks if b.free]

    fid = max(b.bid for b in blocks)

    while fid > 0:
        for i, (start, length) in enumerate(blanks):
            pos, fsize = files[fid]
            if start >= pos:
                # blanks = blanks[:i]
                break
            if fsize == length:
                files[fid] = (start, fsize)
                blanks.pop(i)
                break
            if fsize < length:
                files[fid] = (start, fsize)
                blanks[i] = (start + fsize, length - fsize)
                break
        fid -= 1

    return checksum(Block(fid, pos, size) for fid, (pos, size) in files.items())


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
