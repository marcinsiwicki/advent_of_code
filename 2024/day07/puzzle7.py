"""
Advent of Code 2024: Day 7
"""
import time


def part1(input_eqs: dict) -> int:
    """Determine if + or * operators can be used to achieve result."""
    total_calibrations = 0
    no_match = {}
    for key, vals in input_eqs.items():
        w = [[vals[0]]]
        for i in vals[1:]:
            next_iteration = []
            for j in w[-1]:
                next_iteration.append(j + i)
                next_iteration.append(j * i)
            w.append(next_iteration)
        if key in w[-1]:
            total_calibrations += key
        else:
            no_match[key] = vals

    return total_calibrations, no_match


def part2(input_eqs: dict) -> int:
    """Adding a new operator."""

    total_calibrations = 0
    for key, vals in input_eqs.items():
        w = [[vals[0]]]
        for i in vals[1:]:
            next_iteration = []
            for j in w[-1]:
                next_iteration.append(j + i)
                next_iteration.append(j * i)
                next_iteration.append(int(str(j) + str(i)))
            w.append(next_iteration)
        if key in w[-1]:
            total_calibrations += key

    return total_calibrations


if __name__ == '__main__':
    with open('advent_of_code/2024/day07/input.txt', 'r') as f:
        raw_equations = f.readlines()

    equations = {}
    for l in raw_equations:
        res, inputs = l.split(':')[0], l.split(':')[1]
        equations[int(res)] = [int(i) for i in inputs.split()]

    s = time.time()
    cal_sum, no_match = part1(equations)
    print(f"+ * : {cal_sum} in {time.time() - s}")

    s = time.time()
    addl_sum = part2(no_match)
    print(f"+ * || : {cal_sum + addl_sum} in {time.time() - s}")
