"""
Advent of Code 2024: Day 11
"""
import time
from line_profiler import profile
from functools import cache
from collections import deque


@profile
def part1(stones: list[str], blinks: int = 25) -> int:
    """
    Return number of stones after splitting rules. First rule that applies:
    
    - If the stone is engraved with the number 0, it is replaced by a stone
    engraved with the number 1.
    - If the stone is engraved with a number that has an even number of digits, 
    it is replaced by two stones. The left half of the digits are engraved on 
    the new left stone, and the right half of the digits are engraved on the 
    new right stone. (The new numbers don't keep extra leading zeroes: 1000 would 
    become stones 10 and 0.)
    - If none of the other rules apply, the stone is replaced by a new stone; the 
    old stone's number multiplied by 2024 is engraved on the new stone.

    Args:
        stones (list): list of strings representing stones

    Returns:
        int: count of stones after blinks
    """
    for _ in range(blinks):
        new_stones = []
        for s in stones:
            if s == '0':
                new_stones.append('1')
            elif len(s) % 2 == 0:
                left = s[0:len(s) // 2]
                right = s[len(s) // 2:]
                new_stones.append(str(int(left)))
                new_stones.append(str(int(right)))
            else:
                new_val = int(s) * 2024
                new_stones.append(str(new_val))
        stones = new_stones

    return len(stones)


def part2(stones: list[str], blinks: int = 25) -> int:
    """
    Part1 approach is too slow and mem intensive for Part2.
    """

    @cache
    def expand_stone(input_s):
        """Memoized function to return next stone output."""
        if input_s == '0':
            return '1'
        elif len(input_s) % 2 == 0:
            left = input_s[0:len(input_s) // 2]
            right = input_s[len(input_s) // 2:]
            return (str(int(left)), str(int(right)))
        else:
            new_val = int(input_s) * 2024
            return str(new_val)

    @cache
    def dfs(input_c, n_blink) -> int:
        """Recursive function to calculate given final len of a char and blink."""
        if not isinstance(input_c, tuple):
            input_c = [input_c]

        if n_blink == 0:
            return len(input_c)

        return sum(dfs(expand_stone(i), n_blink-1) for i in input_c)

    stone_len = 0
    for c in stones:
        stone_len += dfs(c, blinks)

    return stone_len


if __name__ == '__main__':
    with open('advent_of_code/2024/day11/input.txt', 'r') as f:
        raw_stones = f.readlines()[0]
    raw_stones = raw_stones.strip().split()

    s = time.time()
    print(f'Number of stones: {part1(raw_stones, 25)} in {time.time() - s}')

    s = time.time()
    print(f'Number of stones: {part2(raw_stones, 75)} in {time.time() - s}')
