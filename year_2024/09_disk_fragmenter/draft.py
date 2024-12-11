from collections import Counter, defaultdict, namedtuple, deque
from copy import deepcopy
from dataclasses import dataclass
import re
from itertools import combinations, product
from math import prod


@dataclass
class Block:
    bid: int
    size: int
    free: bool


@dataclass
class Disk:
    blocks: list[Block]

    def flatten(self):
        blocks = []
        for b in self.blocks:
            blocks += [Block(b.bid, 1, b.free)] * b.size
        return Disk(blocks)

    @property
    def checksum(self):
        csum = 0
        i = 0
        for b in self.blocks:
            for _ in range(b.size):
                csum += i * b.bid if not b.free else 0
                i += 1
        return csum

    def __setitem__(self, i, b):
        self.blocks[i] = b

    def __getitem__(self, i):
        return self.blocks[i]

    def __len__(self):
        return len(self.blocks)

    def __str__(self):
        return "".join(
            str(b.bid) if not b.free else "."
            for b in self.blocks
            for _ in range(b.size)
        )


blocks = []
fid = 0
for i, s in enumerate(open(0).read().strip()):
    s = int(s)
    if i % 2 == 0:
        blocks.append(Block(fid, s, False))
        fid += 1
    else:
        blocks.append(Block(-1, s, True))

disk = Disk(blocks).flatten()

i, j = (0, len(disk) - 1)

while j - i > 1:
    if not disk[j].free:
        while i < j and not disk[i].free:
            i += 1
        if j - i > 1:
            disk[i], disk[j] = disk[j], disk[i]
    j -= 1
print(disk.checksum)


disk = Disk(blocks)

fid = max(b.bid for b in disk.blocks)
# print(disk)
while fid > 1:
    j, bj = next(
        (j, disk[j]) for j in range(len(disk) - 1, -1, -1) if disk[j].bid == fid
    )
    try:
        i, bi = next(
            (i, disk[i]) for i in range(j) if disk[i].free and disk[i].size >= bj.size
        )
        if bi.size == bj.size:
            disk[i], disk[j] = disk[j], disk[i]
        else:
            disk.blocks.insert(i, Block(bj.bid, bj.size, bj.free))
            bi.size -= bj.size
            bj.bid = -1
            bj.free = True
    except StopIteration:
        continue
    finally:
        fid -= 1
        # print(disk)
print(disk.checksum)
