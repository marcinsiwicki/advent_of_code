"""
Advent of Code 2024: Day 22
Monkey Market
"""
from functools import lru_cache


@lru_cache(maxsize=None)
def generate_secret(secret):
    """Helper function to generate next secret."""
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


def part1(buyer_seeds: list[int]) -> int:
    """Compute secrets."""

    N_COUNT = 2000

    total_secrets = 0
    for secret in buyer_seeds:
        for _ in range(N_COUNT):
            secret = generate_secret(secret)
        total_secrets += secret

    return total_secrets


def part2(buyer_seeds: list[int]) -> int:
    """
    Given a secret, find the price and price change and determine 
    overall sell signal and max amount of bananas that can be accumulated.
    """

    N_COUNT = 2000

    total_sequence_dict = {}
    for secret in buyer_seeds:
        eval_sequence = []
        prev_price = secret % 10
        buyer_dict = {}
        for _ in range(N_COUNT):
            secret = generate_secret(secret)
            ones = secret % 10
            if len(eval_sequence) == 4:
                eval_sequence.pop(0)
            eval_sequence.append(ones - prev_price)
            prev_price = ones
            if len(eval_sequence) == 4:
                eval_tuple = tuple(eval_sequence)
                if eval_tuple in buyer_dict:
                    continue
                buyer_dict[eval_tuple] = ones
                if eval_tuple in total_sequence_dict:
                    total_sequence_dict[eval_tuple] += ones
                else:
                    total_sequence_dict[eval_tuple] = ones

    max_value = -1
    for v in total_sequence_dict.values():
        max_value = max(v, max_value)

    return max_value


if __name__ == '__main__':
    with open('advent_of_code/2024/day22/input.txt', 'r') as f:
        seeds = f.readlines()
    seeds = [int(i.strip()) for i in seeds]

    print(f'Total sum of secrets: {part1(seeds)}')
    print(f'Max bananas: {part2(seeds)}')