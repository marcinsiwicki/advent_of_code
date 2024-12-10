"""
Advent of Code 2024: Day 10
"""


KNOWN_PEAKS = set()

def evaluate_trailhead(top_input: list[list[int]], y: int, x: int, peak: int, distinct_paths=False) -> int:
    """
    Given a topographic map and coordinates, trace through path to a peak.

    Args:
        input (list[list[int]]): topographic map 
        y (int): row index
        x (int): col index
        peak (int): search altitude
        distinct_peaks (bool, optional): whether distinct matter. Defaults to True.

    Returns:
        int: peak paths
    """
    global KNOWN_PEAKS
    # search in each direction for a value higher
    if peak == 10:
        if distinct_paths:
            return 1
        if (y, x) in KNOWN_PEAKS:
            return 0
        KNOWN_PEAKS.add((y, x))
        return 1

    n_rows = len(top_input)
    n_cols = len(top_input[0])

    candidates = []
    if y > 0 and 0 <= x < n_cols and top_input[y-1][x] == peak:
        candidates.append([y-1, x])
    if x > 0 and 0 <= y < n_rows and top_input[y][x-1] == peak:
        candidates.append([y, x-1])
    if y < (n_rows - 1) and 0 <= x < n_cols and top_input[y+1][x] == peak:
        candidates.append([y+1, x])
    if x < (n_cols - 1) and 0 <= y < n_rows and top_input[y][x+1] == peak:
        candidates.append([y, x+1])
    if not candidates:
        return 0

    return sum([evaluate_trailhead(top_input, i[0], i[1], peak+1, distinct_paths) for i in candidates])


def part1(topography: list[list[int]]) -> int:
    """
    Return sum of trailhead scores. Trailhead scores are determined by how
    many peaks are reached from a given trailhead. 

    Args:
        topography (list): list of list of string

    Returns:
        int: Sum of each trailhead score.  
    """
    global KNOWN_PEAKS
    # keep a set of the trail coordinates
    # recursive solution of stepping to the next available coordinate
    # iterative of keeping a pointer of where to go back to at each fork


    trailheads = set()
    n_rows = len(topography)
    n_cols = len(topography[0])
    for y in range(n_rows):
        for x in range(n_cols):
            if topography[y][x] == 0: # potential trailhead
                score = evaluate_trailhead(topography, y, x, 1)
                trailheads.add((y, x, score))
                KNOWN_PEAKS = set()

    return sum(i[2] for i in trailheads)


def part2(topography: list[list[int]]) -> int:
    """
    Return similar to part1 but with different call to find all distinct paths.
    """
    trailheads = set()
    n_rows = len(topography)
    n_cols = len(topography[0])
    for y in range(n_rows):
        for x in range(n_cols):
            if topography[y][x] == 0: # potential trailhead
                score = evaluate_trailhead(topography, y, x, 1, True)
                trailheads.add((y, x, score))

    return sum(i[2] for i in trailheads)


if __name__ == '__main__':
    with open('advent_of_code/2024/day10/input.txt', 'r') as f:
        raw_topography = f.readlines()

    # convert to list(list(char))
    raw_topography = [[int(i) for i in l.strip()] for l in raw_topography]
    print(f'Trailhead scores: {part1(raw_topography)}')
    print(f'Trailhead scores (distinct): {part2(raw_topography)}')
