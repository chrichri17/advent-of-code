# https://adventofcode.com/2023/day/7

from collections import Counter


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            hand, bid = line.strip().split(" ")
            yield hand, int(bid)


# fmt: off
CARDS_COUNT: list[tuple[int]] = [
    (5,),             # Five of a kind
    (4, 1),           # Four of a kind
    (3, 2),           # Full house
    (3, 1, 1),        # Three of a kind
    (2, 2, 1),        # Two pair
    (2, 1, 1, 1),     # One Pair
    (1, 1, 1, 1, 1),  # High card
]
# fmt: on
HANDS_KIND = {count: len(CARDS_COUNT) - i for i, count in enumerate(CARDS_COUNT)}


def strength(hand: str, lookup: dict[str, str]):
    return (
        get_hand_kind(hand, lookup),
        [lookup.get(card, card) for card in hand],
    )


def get_hand_kind(hand: str, lookup: dict[str, str]) -> int:
    counts = Counter(hand)
    if lookup["J"] == "*":  # For part 2
        replace_with_joker(counts, lookup)
    cards_count = tuple(sorted(counts.values(), reverse=True))
    return HANDS_KIND[cards_count]


def replace_with_joker(counts: Counter, lookup: dict[str, str]):
    if counts.get("J", 5) < 5:
        # Find the most frequent or highest non-joker card
        max_card = max(
            (card for card in counts if card != "J"),
            key=lambda card: (counts[card], lookup.get(card, card)),
            default=None,
        )

        # Add the count of "J" to the most frequent or highest non-joker card
        counts[max_card] += counts["J"]
        del counts["J"]


def total_winnings(filepath, lookup: dict[str, str]) -> int:
    game = list(read_inputs(filepath))
    game.sort(key=lambda x: strength(x[0], lookup))
    return sum(bid * rank for rank, (_, bid) in enumerate(game, 1))


def part1(filepath) -> int:
    lookup = dict(T="A", J="B", Q="C", K="D", A="E")
    return total_winnings(filepath, lookup)


def part2(filepath) -> int:
    lookup = dict(T="A", J="*", Q="C", K="D", A="E")
    return total_winnings(filepath, lookup)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
