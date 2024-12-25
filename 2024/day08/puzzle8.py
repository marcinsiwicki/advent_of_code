"""
Advent of Code 2024: Day 8
Resonant Collinearity
"""


def part1(input_map, n_rows, n_cols):
    """
    Find antinodes within map.

    Antinodes appear when the same antenna type is present in a line and one
    elem is X away and the nex is 2x away is there an open cell that is in a
    direction of line from an antenna
    """
    antinodes = set()
    for ants in input_map.values():
        for ant_1 in ants:
            for ant_2 in ants:
                if ant_1 == ant_2:
                    continue
                ant_1_x, ant_1_y = ant_1[1], ant_1[0]
                ant_2_x, ant_2_y = ant_2[1], ant_2[0]
                rise = ant_2_y - ant_1_y
                run = ant_2_x - ant_1_x

                tgt_x = (2 * run) + ant_1_x
                tgt_y = (2 * rise) + ant_1_y
                if -1 < tgt_y < n_rows and -1 < tgt_x < n_cols:
                    antinodes.add((tgt_y, tgt_x))

    return antinodes


def part2(input_map, n_rows, n_cols):
    """Find antinodes within map ignoring distance requirement."""
    antinodes = set()
    for ants in input_map.values():
        for ant_1 in ants:
            for ant_2 in ants:
                if ant_1 == ant_2:
                    continue
                ant_1_x, ant_1_y = ant_1[1], ant_1[0]
                ant_2_x, ant_2_y = ant_2[1], ant_2[0]
                rise = ant_2_y - ant_1_y
                run = ant_2_x - ant_1_x

                n = 1
                # find max number of iterations in a given dir
                if rise < 0:
                    max_rise = (ant_1_y / abs(rise)) - 1
                else:
                    max_rise = abs((n_rows - ant_1_y) / rise)
                if run < 0:
                    max_run = (ant_1_x / abs(run)) - 1
                else:
                    max_run = abs((n_cols - ant_1_x) / run)

                while n <= min(max_rise, max_run) + 1:
                    tgt_x = (n * run) + ant_1_x
                    tgt_y = (n * rise) + ant_1_y
                    if -1 < tgt_y < n_rows and -1 < tgt_x < n_cols:
                        antinodes.add((tgt_y, tgt_x))
                    n += 1

    return antinodes


if __name__ == '__main__':
    with open('advent_of_code/2024/day08/input.txt', 'r') as f:
        coors = f.readlines()

    # convert to dict of antenna type and matrix index
    coors = [list(l.strip()) for l in coors]
    n_rows = len(coors)
    n_cols = len(coors[0])
    coors_map = {}
    for i in range(n_rows):
        for j in range(n_cols):
            check_char = coors[i][j]
            if check_char == '.':
                continue
            if check_char in coors_map:
                coors_map[check_char].append((i, j))
            else:
                coors_map[check_char] = [(i, j)]

    res = part1(coors_map, n_rows, n_cols)
    print(f'Number of antinodes: {len(res)}')
    res = part2(coors_map, n_rows, n_cols)
    print(f'Number of antinodes with resonance: {len(res)}')
