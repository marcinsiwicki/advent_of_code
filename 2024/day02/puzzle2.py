"""
Advent of Code 2024: Day 2
"""

MIN_INC = 1     # minimum step size
MAX_INC = 3     # maximum step size

def check_range(start_value: int, eval_value: int) -> bool:
    """Given two inputs, check that distance between values conforms to expectations."""
    if eval_value < start_value:
        return False

    return (start_value + MIN_INC) <= eval_value <= (start_value + MAX_INC)


def part1(reports_: list) -> int:
    """Determine baseline safety of report."""
    safe_reports = 0

    for level in reports_:
        # check that numbers are either increasing or decreasing
        # adjacent numbers must be > 1 or <= 3 different

        # if second elem is less than first then reverse list to get the new order
        if level[1] < level[0]:
            level = level[-1::-1]

        i = 0
        j = 1

        while j < len(level):
            if check_range(level[i], level[j]):
                i += 1
                j += 1
            else:
                break

        if j == len(level):
            safe_reports += 1

    return safe_reports


def part2(reports_: list) -> int:
    """Determine safety if up to one level can be removed."""
    safe_reports = 0

    for level in reports_:
        # loosely order list
        # determine if list should be increasing or decreasing by number of pairwise changes

        diffs = []
        for i in range(len(level) - 1):
            diffs.append(level[i+1] - level[i])
        if sum(i for i in diffs if i > 0) < abs(sum(i for i in diffs if i < 0)):
            level = level[-1::-1]

        i = 0
        j = 1
        problem_dampened = False

        while j < len(level):
            if check_range(level[i], level[j]):
                i += 1
                j += 1
            elif not problem_dampened:
                # basically there are the following cases:
                #   - the next element is bad
                #         i and next+1 are correct
                #   - the current element is bad
                #         i-1 and next are correct

                # if its at end of list, continue
                if j+1 == len(level):
                    problem_dampened = True
                    j += 1
                    continue
                # the next element is bad
                if check_range(level[i], level[j+1]):
                    level.pop(j)
                    problem_dampened = True
                # the current element is bad
                elif check_range(level[j], level[j+1]):
                    if i == 0: # if the first element is bad we can just pop
                        level.pop(i)
                        problem_dampened = True
                    elif check_range(level[i-1], level[j]): # if its in the list and bad, need to check prior
                        level.pop(i)
                        problem_dampened = True
                    else:
                        break
                else:
                    break
            else:
                break

        if j == len(level):
            safe_reports += 1

    return safe_reports


if __name__ == '__main__':
    with open('advent_of_code/day02/input.txt', 'r', encoding='utf-8') as f:
        reports = f.readlines()
    reports = [level.replace('\n', '').split(' ') for level in reports]
    reports = [[int(i) for i in level] for level in reports]

    print('Part 1: ', part1(reports))
    print('Part 2: ', part2(reports))
