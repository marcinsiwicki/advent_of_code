"""
Advent of Code 2024: Day 7
"""
import math
import itertools


def part1(input_eqs: dict) -> int:
    """Determine if + or * operators can be used to achieve result."""

    operators = {'+': sum,
                 '*': math.prod
                 }

    total_calibrations = 0
    no_match = {}
    for key, vals in input_eqs.items():
        valid_match = False

        if sum(vals) == key: # all sums
            total_calibrations += key
            valid_match = True
        elif math.prod(vals) == key: # all prods
            total_calibrations += key
            valid_match = True
        else: # mixed
            # work left to right and try operators
            n_ops = len(vals) - 1
            cartesian = list(itertools.product(['+', '*'], repeat=n_ops))
            cartesian = [list(l) for l in cartesian]
            for seq in cartesian:
                if seq == ['*'] * n_ops or seq == ['+'] * n_ops:
                    continue
                w = vals[0]
                for n in vals[1:]:
                    w = operators[seq.pop()]([w, n])
                if w == key:
                    total_calibrations += key
                    valid_match = True
                    break

        if not valid_match:
            no_match[key] = vals

    return total_calibrations, no_match


def part2(input_eqs: dict) -> int:
    """Adding a new operator."""

    def pipe(n):
        return int(str(n[0]) + str(n[1]))

    operators = {'+': sum,
                 '*': math.prod,
                 '||': pipe
                 }

    total_calibrations = 0
    for key, vals in input_eqs.items():
        n_ops = len(vals) - 1
        cartesian = list(itertools.product(['+', '*', '||'], repeat=n_ops))
        cartesian = [list(l) for l in cartesian]
        for seq in cartesian:
            w = vals[0]
            for n in vals[1:]:
                w = operators[seq.pop()]([w, n])
            if w == key:
                total_calibrations += key
                break

    return total_calibrations


if __name__ == '__main__':
    with open('advent_of_code/2024/day07/input.txt', 'r') as f:
        raw_equations = f.readlines()

    equations = {}
    for l in raw_equations:
        res, inputs = l.split(':')[0], l.split(':')[1]
        equations[int(res)] = [int(i) for i in inputs.split()]

    cal_sum, no_match = part1(equations)
    print(f"+ * : {cal_sum}")

    addl_sum = part2(no_match)
    print(f"+ * || : {cal_sum + addl_sum}")
