"""
Advent of Code 2023: Day 4
"""

def part1(cards: list) -> int:
    """Sum scores per card."""
    total_tally = 0
    for card in cards:
        numbers = card.split(':')[1]
        winners, entries = numbers.split('|')
        winners = winners.split()
        entries = entries.split()

        matches = [e for e in entries if e in winners]
        if matches:
            total_tally += 1 * max(1, 2**(len(matches)-1))

    return total_tally


def part2(cards: list) -> int:
    """Find copies of cards and see how many total cards you collect at the end."""
    n_orig = len(cards) # make sure not to go past end of table

    # build map of number of winners per card to avoid recomputation
    card_wins = {}
    for card in cards:
        i, numbers = card.split(':')
        i = int(i.replace('Card', ''))

        winners, entries = numbers.split('|')
        winners = winners.split()
        entries = entries.split()

        matches = [e for e in entries if e in winners]
        card_wins[i] = len(matches)

    cards_to_proc = list(card_wins.keys())
    for card in cards_to_proc:
        n_wins = card_wins[card]

        cards_to_add = cards_to_proc[card:min(n_orig, card+n_wins)]
        cards_to_proc += cards_to_add

    return len(cards_to_proc)


if __name__ == '__main__':
    with open('advent_of_code/2023/day04/input.txt', 'r') as f:
        scratch_cards = f.readlines()

    print(f"Scratch cards score: {part1(scratch_cards)}")
    print(f"Scratch card count: {part2(scratch_cards)}")
