"""
Advent of Code 2023: Day 1
"""
import re


def part1(input_list: list) -> int:
    """Return total sum of first and last digit on each line."""
    total_sum = 0
    for l in input_list:
        nums = re.findall(r"\d", l)
        total_sum += int(nums[0] + nums[-1])

    return total_sum


def part2(input_list: list) -> int:
    """Convert text to int and compute sum."""
    valid_words = {"one": "1",
                   "two": "2",
                   "three": "3",
                   "four": "4",
                   "five": "5",
                   "six": "6",
                   "seven": "7",
                   "eight": "8",
                   "nine": "9"
                   }

    # regex needs to handle overlap such as sevenine
    pattern = r"(?=(\d|" + "|".join(valid_words.keys()) + "))"
    total_sum = 0

    for l in input_list:
        nums = re.findall(pattern, l)
        left, right = nums[0], nums[-1]

        left = valid_words.get(left, left)
        right = valid_words.get(right, right)

        total_sum += int(left + right)

    return total_sum


if __name__ == '__main__':
    with open('advent_of_code/2023/day01/input.txt', 'r') as f:
        inputs = f.readlines()

    print(part1(inputs))
    print(part2(inputs))