"""
Advent of Code 2024: Day 3
Mull It Over
"""
import re


def part1(instrs: list) -> int:
    """Identify multiply instructions and return sum of products."""
    pattern = r"mul\(\d{1,3},\d{1,3}\)"
    product = 0
    for line in instrs:
        if matches := re.findall(pattern, line):
            nums = [re.findall(r"\d{1,3}", mul) for mul in matches]
            product += sum(int(n[0]) * int(n[1]) for n in nums)

    return product


def part2(instrs: list) -> int:
    """Identify enable/disable of multiply instructions. Return sum of products."""
    pattern = r"mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)"

    product = 0
    enable_mult = True

    for line in instrs:
        if matches := re.findall(pattern, line):
            for instr in matches:
                if instr == "don't()":
                    enable_mult = False
                elif instr == "do()":
                    enable_mult = True
                else: # mul() instructions
                    if enable_mult:
                        nums = re.findall(r"\d{1,3}", instr)
                        product += int(nums[0]) * int(nums[1])

    return product


if __name__ == '__main__':
    with open('advent_of_code/2024/day03/input.txt', 'r', encoding='utf-8') as f:
        instructions = f.readlines()

    print(f"Part 1 Product is {part1(instructions)}")
    print(f"Part 2 Product is {part2(instructions)}")
