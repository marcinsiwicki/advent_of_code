"""
Advent of Code 2024: Day 21
Keypad Conundrum

Need to use a directional keypad to control a directional keypad
to control an alphanum keypad. Failure condition if at any point you
manuever to an empty part of the grid.

The key is that all subsequences end in A. If we can operate on these subsequences
can recursively DFS to the human level. 

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
from functools import lru_cache
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
    """Which grid to use for shortest path"""
    ALPHANUM = 1
    DPAD = 2


@lru_cache(maxsize=None)
def _find_shortest_path(pad_type: KeypadType, start: str,
                        target: str, append_a=True) -> list[list[str]]:
    """
    Shortest path implementation. Returns all shortest paths within given grid.

    Args:
        pad_type (KeypadType): indicates to search in keypad or dpad 
        start (str): starting character in grid
        target (str): ending character in grid
        append_a (bool, optional): if final resting 'A' should be appended to path

    Returns:
        list[list[str]]: translation of directions needed to travel on keypad 
                         projected a layer down.
    """
    if pad_type == KeypadType.ALPHANUM:
        grid = ALPHANUM_GRID
    elif pad_type == KeypadType.DPAD:
        grid = DPAD_GRID

    visited = set()
    distances = {n: float('inf') for n in grid} | {start: 0}
    best_paths = []
    best_dist = float('inf')

    pq = [(0, start, [start], None)]

    while pq:
        dist, node, path, d = heapq.heappop(pq)
        if (node, d) in visited:
            continue
        if node == target:
            if dist < best_dist:
                best_paths = [path]
                best_dist = dist
            elif dist <= best_dist:
                best_paths.append(path)
        visited.add((node, d))
        for neighbor in grid[node]:
            new_dist = dist
            new_dir = grid[node][neighbor]
            if new_dir != d:
                new_dist = dist + 1 # want to prioritize not turning
            if new_dist <= distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor], new_dir))

    # convert to the directional symbol
    translated_paths = []
    for best_path in best_paths:
        lookup = grid[start]
        translated_path = []
        for n in best_path[1:]:
            translated_path.append(lookup[n])
            lookup = grid[n]
        translated_paths.append(translated_path)

    if append_a:
        translated_paths = [path + ['A'] for path in translated_paths]
        return translated_paths
    return translated_paths


def _unwind_directional(target_path):
    """
    Helper function to expand directional path and create subsequences 
    ending in A.
    """
    start = 'A'
    sequence = []

    for seq in target_path:
        for entry in seq:
            paths = _find_shortest_path(KeypadType.DPAD, start, entry, append_A=False)
            start = entry
            sequence.append(paths)

    sequence_chunks = []
    for chunk in sequence:
        tmp = []
        for n in chunk:
            tmp.append(list(n) + ['A'])
        sequence_chunks.append(tmp)

    return sequence_chunks


@lru_cache(maxsize=None)
def _unwind_robot(target_path, n_iters):
    """Recursive function to traverse to highest level robot."""
    if n_iters == 0:
        return len(target_path)

    subseq_paths = _unwind_directional(target_path)

    total_len = 0
    for chunk in subseq_paths:
        tmp = float('inf')
        for seq in chunk:
            res = _unwind_robot(tuple(seq), n_iters-1)
            tmp = min(tmp, res)
        total_len += tmp

    return total_len


def _find_base_keypad_path(code):
    """Helper function to find the base path of root robot."""
    code_path = []
    start = 'A'
    for entry in code:
        path = _find_shortest_path(KeypadType.ALPHANUM, start, entry)
        start = entry
        code_path.append(path)
    return code_path


def part2(codes: list[str], n_iters: int) -> int:
    """
    Primary function to find base keypad shortest path and then provide
    to recursive function in determining shortest path after unwinds.
    """
    input_lens = {}
    for code in codes:
        target_path = _find_base_keypad_path(code)

        # now we have to get the button presses that will return the above
        target_len = 0
        for chunk in target_path:
            target_len += min(_unwind_robot(tuple(seq), n_iters) for seq in chunk)

        input_lens[code] = target_len

    complexity = 0
    for k, v in input_lens.items():
        k_int = int(k.split('A')[0])
        complexity += k_int * v

    return complexity


if __name__ == '__main__':
    with open('advent_of_code/2024/day21/input.txt', 'r') as f:
        codes = f.readlines()
    codes = [c.strip() for c in codes]

    s = time.time()
    ITERS = 2
    print(f'Complexity of codes: {part2(codes, ITERS)} in {time.time() - s}')

    s = time.time()
    ITERS = 25
    print(f'Complexity of codes (n={ITERS}): {part2(codes, ITERS)} in {time.time() - s}')
