"""
Advent of Code 2024: Day 1 
"""
import collections

def part1(left: list, right: list) -> int:
    """Calculate pairwise difference"""

    lens = [abs(i[0] - i[1]) for i in zip(left, right)]

    return sum(lens)


def part2(left: list, right: list) -> int:
    """Return similarity score."""

    right_map = collections.Counter(right)
    sim_scores = [i * right_map[i] for i in left if i in right_map] 

    return sum(sim_scores)


if __name__ == '__main__':
    with open('advent_of_code/day01/input.txt', 'r', encoding='utf-8') as f:
        locations = f.readlines()

    # convert to list(list(int))
    locations = [[int(l.split(' ')[0]), int(l.split(' ')[-1].strip())] for l in locations]
    left_list = sorted([l[0] for l in locations])
    right_list = sorted([l[1] for l in locations])

    print(part1(left_list, right_list))
    print(part2(left_list, right_list))
