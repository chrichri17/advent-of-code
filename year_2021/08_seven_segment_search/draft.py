from collections import Counter, defaultdict, namedtuple
from copy import deepcopy
from dataclasses import dataclass
import re
from itertools import permutations


values = "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdfeg abcdfg".split()

zero, one, two, three, four, five, six, seven, eight, nine = values
digits = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

reversed_digits = {v: k for k, v in digits.items()}

DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


# 6 on
# zero: abcefg
# six:  abdefg
# nine: abcdfg

# 5 on
# two:   acdeg
# three: acdfg
# five:  abdfg

# 4 on
# four: bcdf

# 3 on
# seven: acf

# 2 on
# one: cf

# 7 on
# eight: abcdefg

total = 0
for line in open(0).read().splitlines():
    l, r = line.split(" | ")
    l = l.split()
    r = r.split()

    the_eight = [x for x in l if len(x) == 7][0]
    the_one = [x for x in l if len(x) == 2][0]
    the_four = [x for x in l if len(x) == 4][0]
    the_seven = [x for x in l if len(x) == 3][0]

    # 7 and 1 can let you know what is a
    diff = set(the_seven) - set(the_one)
    assert len(diff) == 1
    a = diff.pop()
    debug("a ->", a)

    all_sixes = [x for x in l if len(x) == 6]
    assert len(all_sixes) == 3
    inter = set(all_sixes[0]) & set(all_sixes[1]) & set(all_sixes[2])  # this gives abfg
    assert len(inter) == 4, "expected intersection of all sixes to be of length 4"
    # but inter -  4 - 7 is g
    diff = inter - set(the_four) - set(the_seven)
    assert len(diff) == 1
    g = diff.pop()
    debug("g ->", g)

    all_fives = [x for x in l if len(x) == 5]
    inter = set(all_fives[0]) & set(all_fives[1]) & set(all_fives[2])  # this gives adg
    assert len(inter) == 3, "expected intersection of all fives to be of length 3"
    # but inter - a - g is d
    diff = inter - {a} - {g}
    assert len(diff) == 1
    d = diff.pop()
    debug("d ->", d)

    # 4 - 7 - d is b
    diff = set(the_four) - set(the_seven) - {d}
    assert len(diff) == 1
    b = diff.pop()
    debug("b ->", b)

    inter = set(all_sixes[0]) & set(all_sixes[1]) & set(all_sixes[2])  # this gives abfg
    assert len(inter) == 4, "expected intersection of all sixes to be of length 4"
    # but we know a, b and g
    diff = inter - {a} - {b} - {g}
    assert len(diff) == 1
    f = diff.pop()
    debug("f ->", f)

    # now we know c from 1
    diff = set(the_one) - {f}
    assert len(diff) == 1
    c = diff.pop()
    debug("c ->", c)

    # now we know e from 8
    diff = set(the_eight) - {a} - {b} - {c} - {d} - {f} - {g}
    assert len(diff) == 1
    e = diff.pop()
    debug("e ->", e)

    mapping = {a: "a", b: "b", c: "c", d: "d", e: "e", f: "f", g: "g"}

    assert len(list(mapping.keys())) == 7, debug(a, b, c, d, e, f, g)

    out = []
    for x in r:
        drepr = "".join(sorted([mapping[xx] for xx in x]))
        # print(drepr)
        out.append(str(reversed_digits[drepr]))
    out = "".join(out)

    print(out)
    total += int(out)

print(total)
