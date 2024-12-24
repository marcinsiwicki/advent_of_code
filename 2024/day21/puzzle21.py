"""
Advent of Code 2024: Day 21
Keypad Conundrum

Need to use a directional keypad to control a directional keypad
to control an alphanum keypad. Failure condition if at any point you
manuever to an empty part of the grid.

[[7  , 8,   9 ],
 [4  , 5,   6 ],
 [1  , 2,   3 ],
 [' ', 0,  'A']]

[[' ', '^', 'A'],
 ['<', 'v', '>']]

Line 4: 456A
v<<A^>>AAv<A<A^>>AAvAA^<A>Av<A^>A<A>Av<A^>A<A>Av<<A>A^>AAvA^<A>A [human]
   <   AA  v <   AA >>  ^ A  v  A ^ A  v  A ^ A   < v  AA >  ^ A [robot 3]
       ^^        <<       A     >   A     >   A        vv      A [robot 2]
                          4         5         6                A [keypad robot]
string length=64
Complexity: 456 x 64 = 29184

Line 5: 379A
v<<A^>>AvA^Av<A<AA^>>AAvA^<A>AAvA^Av<A^>AA<A>Av<<A>A^>AAAvA^<A>A
   <   A > A  v <<   AA >  ^ AA > A  v  AA ^ A   < v  AAA >  ^ A
       ^   A         <<      ^^   A     >>   A        vvv      A
           3                      7          9                 A
string length=64
Complexity: 379 x 64 = 24256
"""
from enum import Enum
from functools import cache, lru_cache
import time
import heapq


DPAD_GRID = {
    '<': {'v': '>'},
    'v': {'<': '<', '>': '>', '^': '^'},
    '^': {'v': 'v', 'A': '>'},
    '>': {'v': '<', 'A': '^'},
    'A': {'^': '<', '>': 'v'},
}

ALPHANUM_GRID = {
   'A': {'0': '<', '3': '^'},
   '0': {'A': '>', '2': '^'},
   '1': {'4': '^', '2': '>'},
   '2': {'1': '<', '5': '^', '0': 'v', '3': '>'},
   '3': {'2': '<', '6': '^', 'A': 'v'},
   '4': {'7': '^', '5': '>', '1': 'v'},
   '5': {'4': '<', '8': '^', '6': '>', '2': 'v'},
   '6': {'5': '<', '9': '^', '3': 'v'},
   '7': {'4': 'v', '8': '>'},
   '8': {'7': '<', '5': 'v', '9': '>'},
   '9': {'8': '<', '6': 'v'}, 
}


class KeypadType(Enum):
    ALPHANUM = 1
    DPAD = 2


# @lru_cache(maxsize=None)
def _find_shortest_path(pad_type, start: str, target: str):
    # grid weights need to be result of unpacked length rather than
    # single path on current keypad
    if pad_type == 1: #KeypadType.ALPHANUM:
        grid = ALPHANUM_GRID
    elif pad_type == 2: #KeypadType.DPAD:
        grid = DPAD_GRID

    visited = set()
    distances = {n: float('inf') for n in grid}
    distances[start] = 0
    best_path = []
    best_dist = float('inf')
    pq = [(0, start, [start], None)]

    while pq:
        dist, node, path, d = heapq.heappop(pq)
        if (node, d) in visited:
            continue
        if node == target:
            if dist < best_dist:
                best_path = path
                best_dist = dist
        visited.add((node, d))
        for neighbor in grid[node]:
            new_dist = dist
            new_dir = grid[node][neighbor]
            if new_dir != d:
                new_dist = dist + 1
            if new_dist <= distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor], new_dir))

    translated_path = []
    lookup = grid[start]
    for n in best_path[1:]:
        translated_path.append(lookup[n])
        lookup = grid[n]
    return tuple(translated_path + ['A'])



def part1(codes: list[str]) -> int:
    # starting with final robot, determine the key presses that get you to
    # target code entry in least moves possible.
    # push that new code sequence up one level and find the shortest path through
    # repeat

    input_lens = {}

    for code in codes:
        code_path = []
        start = 'A'
        for entry in code:
            path = _find_shortest_path(1, start, entry)
            start = entry
            code_path += path

        # now we have to get the button presses that will return the above
        dpad_path = []
        start = 'A'
        for entry in code_path:
            path = _find_shortest_path(2, start, entry)
            start = entry
            dpad_path += path

        dpad2_path = []
        start = 'A'
        for entry in dpad_path:
            path = _find_shortest_path(2, start, entry)
            start = entry
            dpad2_path += path

        input_lens[code] = dpad2_path

    complexity = 0
    for k, v in input_lens.items():
        k_int = int(k.split('A')[0])
        complexity += k_int * len(v)

    return complexity


@lru_cache(maxsize=None)
def unwind_robot(target_path, n_iters):
    # print('target_path', target_path, n_iters)
    if n_iters == 0:
        # print('return', target_path)
        return len(target_path)

    start = 'A'
    total_len = 0
    splits = [i+1 for i, c in enumerate(target_path) if c == 'A']

    subseq_paths = []
    prev = 0
    for i in splits:
        subseq_paths.append(target_path[prev:i])
        prev = i

    # for entry in target_path:
    for subseq in subseq_paths:
        dpad_path = []
        for entry in subseq:
            path = _find_shortest_path(2, start, entry)
            dpad_path += path
            # print(target_path, entry, start, n_iters, path)
            start = entry
        total_len += min(unwind_robot(tuple(dpad_path), n_iters-1) for p in path)

    return total_len


def part2(codes: list[str], n_iters) -> int:
    input_lens = {}
    for code in codes:
        code_path = []
        start = 'A'
        for entry in code:
            path = _find_shortest_path(1, start, entry)
            start = entry
            code_path += path

        # now we have to get the button presses that will return the above
        target_path = code_path
        target_path = unwind_robot(tuple(target_path), n_iters)

        input_lens[code] = target_path

    complexity = 0
    for k, v in input_lens.items():
        print(k, v)
        k_int = int(k.split('A')[0])
        complexity += k_int * v

    return complexity


if __name__ == '__main__':
    with open('advent_of_code/2024/day21/test.txt', 'r') as f:
        codes = f.readlines()
    codes = [c.strip() for c in codes]

    s = time.time()
    print(f'Complexity of codes: {part1(codes)} in {time.time() - s}')
    s = time.time()
    iters = 3
    print(f'Complexity of codes (n={iters}): {part2(codes, iters)} in {time.time() - s}')

    # print(unwind_robot(('^', '^', '<', '<', 'A'), 2))