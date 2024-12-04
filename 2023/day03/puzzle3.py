"""
Advent of Code 2023: Day 3
"""
import re


def part1(schem: list) -> int:
    """
    Compute sum of part numbers.
    Need to parse out digits that exist and then check if characters around
    Those digits (including diagonally) have a symbol

    Extract each number per line and symbols. compute if symbol is adjacent
    To number including lines above/below
    For instance 35 is line 3, idx 3 and len 2 so we check
        line 2:1-4, line 3: 1, 4, line 4:1-4
    Store data as lines = [number, line, index]
    """
    raw_nums = []
    for i, line in enumerate(schem):
        for match in re.finditer(r"\d+", line):
            raw_nums.append([match.group(), i, match.start(), match.end()])

    total = 0
    pattern = r"[^.\d\n]"
    for num in raw_nums:
        # at most two additional lines
        part, line, idx_start, idx_end = num

        # check same line
        to_check = schem[line][max(idx_start-1, 0):min(idx_end+1, len(schem[line]))]
        include = re.findall(pattern, to_check)

        # check prev line
        if not include and line > 0:
            to_check = schem[line-1][max(idx_start-1, 0):min(idx_end+1, len(schem[line-1]))]
            include = re.findall(pattern, to_check)

        # check next line
        if not include and line < len(schem)-1:
            to_check = schem[line+1][max(idx_start-1, 0):min(idx_end+1, len(schem[line+1]))]
            include = re.findall(pattern, to_check)

        if include:
            total += int(part)

    return total


def part2(schem: list) -> int:
    """
    Find gear ratios!
    Gears are adjacent to exactly two part numbers.
    Build a map of the numbers and their adjacent equivalent indicies.
    """
    raw_nums = {}
    for i, line in enumerate(schem):
        raw_nums[i] = []
        for match in re.finditer(r"\d+", line):
            raw_nums[i].append([match.group(),
                                max(0, match.start()-1),
                                min(match.end(), len(line))
            ])

    gear_ratio = 0
    for i, line in enumerate(schem):
        for gear in re.finditer(r"\*", line):
            gear_idx = gear.start()
            matching_nums = []
            potential_lines = [] #instantiate the list otherwise it will append to original map

            potential_lines += raw_nums.get(i)
            if i > 0:
                potential_lines += raw_nums.get(i-1)
            if i < len(schem):
                potential_lines += raw_nums.get(i+1)

            for num in potential_lines:
                part_no, part_start, part_end = num
                if part_start <= gear_idx <= part_end:
                    matching_nums.append(int(part_no))

            if len(matching_nums) == 2:
                gear_ratio += matching_nums[0] * matching_nums[1]

    return gear_ratio


if __name__ == '__main__':
    with open('advent_of_code/2023/day03/input.txt', 'r') as f:
        schematic = f.readlines()

    print(f"Sum of part numbers {part1(schematic)}")
    print(f"Gear ratio: {part2(schematic)}")
