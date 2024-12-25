"""
Advent of Code 2024: Day 25
Code Chronicle
"""


def part1(locks: list[list[str]], keys: list[list[str]]) -> int:
    """
    Return the number of locks and keys that have valid pin orientations
    without overlap.
    """
    lock_key_pairs = 0

    for lock in locks:
        for key in keys:
            n_rows = len(lock)
            n_cols = len(lock[0])
            all_pins_fit = []
            for col in range(n_cols):
                lock_sum = sum(1 for i in lock if i[col] == '#')
                key_sum = sum(1 for i in key if i[col] == '#')
                if (lock_sum + key_sum) <= n_rows:
                    all_pins_fit.append(True)
                else:
                    all_pins_fit.append(False)
            if all(all_pins_fit):
                lock_key_pairs += 1

    return lock_key_pairs


if __name__ == '__main__':
    with open('advent_of_code/2024/day25/input.txt', 'r') as f:
        schematics = f.read().split('\n\n')

    locks, keys = [], []
    for schema in schematics:
        grid = schema.split('\n')
        if all(i == '#' for i in grid[0]):
            locks.append(grid)
        else:
            keys.append(grid)

    print(f'Matching locks and keys: {part1(locks, keys)}')
