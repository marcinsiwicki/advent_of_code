"""
Advent of Code 2024: Day 19
Linen Layout
"""
import time
from functools import lru_cache


@lru_cache(maxsize=None)
def build_pattern(target_pattern: str, towels: tuple(str)):
    """Recursive helper function to determine if pattern can be made from strings."""
    if target_pattern == '':
        return 1
    potential_paths = []
    for towel in towels:
        if target_pattern.startswith(towel):
            potential_paths.append(towel)
    if potential_paths:
        return sum(build_pattern(target_pattern.removeprefix(t), towels) for t in potential_paths)
    return 0


def part1(towels: tuple[str], pattern_requests: list[str]) -> int:
    """
    Return number of pattern requests possible given towel combinations.

    Args:
        towels (tuple[str]): towels available at onsen
        pattern_requests (list[str]): patterns onsen wants to display

    Returns:
        int: how many of the patterns can be made
    """
    # use avail towels to pattern match into the pattern requests
    # only care about whether or not the pattern is achievable rather than how

    possible_patterns = 0
    for pattern in pattern_requests:
        if build_pattern(pattern, towels) > 0:
            possible_patterns += 1

    return possible_patterns


def part2(towels: tuples[str], pattern_requests: list[str]) -> int:
    """
    Return the number of ways each pattern can be made.

    Args:
        towels (tuples[str]): towels available at the onsen
        pattern_requests (list[str]): patterns the onsen wants to display

    Returns:
        int: how many ways each pattern can be made 
    """
    # use avail towels to pattern match into the pattern requests
    # only care about whether or not the pattern is achievable rather than how

    possible_patterns = 0
    for pattern in pattern_requests:
        possible_patterns += build_pattern(pattern, towels)

    return possible_patterns


if __name__ == '__main__':
    with open('advent_of_code/2024/day19/input.txt', 'r') as f:
        towels, pattern_requests = f.read().split('\n\n')

    towels = tuple(towels.replace(' ', '').split(','))
    pattern_requests = pattern_requests.split()

    s = time.time()
    print(f'Possible matches: {part1(towels, pattern_requests)} in {time.time() - s}')
    s = time.time()
    print(f'Total orientations: {part2(towels, pattern_requests)} in {time.time() - s}')
