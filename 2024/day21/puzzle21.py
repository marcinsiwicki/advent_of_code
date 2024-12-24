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


numeric_pos = {"7": (0, 0), "8": (0, 1), "9": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2),
               "1": (2, 0), "2": (2, 1), "3": (2, 2), None: (3, 0), "0": (3, 1), "A": (3, 2)}
directional_pos = {None: (0, 0), "^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


def sanitize_paths(paths, p0, numeric=True):

    excluded_pos = numeric_pos[None] if numeric else directional_pos[None]

    i = 0
    while i < len(paths):
        p = list(p0)
        for d in paths[i]:

            if d == "^":
                p[0] -= 1
            if d == "v":
                p[0] += 1

            if d == "<":
                p[1] -= 1
            if d == ">":
                p[1] += 1
            
            if tuple(p) == excluded_pos:
                paths.pop(i)
                i -= 1
                break
        
        i += 1

    return paths


def get_shortest_paths(src_pos, trg_pos, numeric=True):
    cx = "^" if trg_pos[0] - src_pos[0] < 0 else "v"
    dx = abs(trg_pos[0] - src_pos[0])
    cy = "<" if trg_pos[1] - src_pos[1] < 0 else ">"
    dy = abs(trg_pos[1] - src_pos[1])

    return sanitize_paths(list(set([cx * dx + cy * dy, cy * dy + cx * dx])), src_pos, numeric=numeric)

def solve_directional(seq):
    pos = directional_pos["A"]

    sequence = []

    for chunk in seq:
        for n in chunk:
            p = directional_pos[n]
            paths = get_shortest_paths(pos, p, numeric=False)
            pos = p
            sequence.append(paths)

    sequence_parts = []
    for part in sequence:
        tmp = []
        for p in part:
            tmp.append("".join(p) + "A")

        sequence_parts.append(tmp)

    return sequence_parts


# @lru_cache(maxsize=None)
def _find_shortest_path(pad_type, start: str, target: str, append_A=True):
    # grid weights need to be result of unpacked length rather than
    # single path on current keypad
    if pad_type == 1: #KeypadType.ALPHANUM:
        grid = ALPHANUM_GRID
    elif pad_type == 2: #KeypadType.DPAD:
        grid = DPAD_GRID

    visited = set()
    distances = {n: float('inf') for n in grid}
    distances[start] = 0
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
                new_dist = dist + 1
            if new_dist <= distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor], new_dir))

    translated_paths = []
    for best_path in best_paths:
        lookup = grid[start]
        translated_path = []
        for n in best_path[1:]:
            translated_path.append(lookup[n])
            lookup = grid[n]
        translated_paths.append(translated_path)

    if append_A:
        translated_paths = [path + ['A'] for path in translated_paths]
        return translated_paths
    else:
        return translated_paths



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
            code_path.append(path)

        # now we have to get the button presses that will return the above
        target_path = code_path
        target_len = 0
        for chunk in target_path:
            target_len += min([unwind_robot(tuple(seq), 2) for seq in chunk])
        # target_path = unwind_robot(tuple(target_path), 1)

        # input_lens[code] = target_path
        input_lens[code] = target_len 

    complexity = 0
    for k, v in input_lens.items():
        print(k, v)
        k_int = int(k.split('A')[0])
        complexity += k_int * v

    return complexity


    # input_lens = {}

    # for code in codes:
    #     code_path = []
    #     start = 'A'
    #     for entry in code:
    #         path = _find_shortest_path(1, start, entry)
    #         start = entry
    #         code_path += path

    #     # now we have to get the button presses that will return the above
    #     dpad_path = []
    #     start = 'A'
    #     for seq in code_path:
    #         for entry in seq:
    #             path = _find_shortest_path(2, start, entry)
    #             start = entry
    #             dpad_path += path

    #     dpad2_path = []
    #     start = 'A'
    #     for seq in dpad_path:
    #         for entry in seq:
    #             path = _find_shortest_path(2, start, entry)
    #             start = entry
    #             dpad2_path += path

    #     input_lens[code] = dpad2_path

    # complexity = 0
    # for k, v in input_lens.items():
    #     print(k, len(v))
    #     k_int = int(k.split('A')[0])
    #     complexity += k_int * len(v)

    # return complexity


def _unwind_directional(target_path):
    start = 'A'
    sequence = []

    for seq in target_path:
        for entry in seq:
            paths = _find_shortest_path(2, start, entry, append_A=False)
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
def unwind_robot(target_path, n_iters):
    # print('target_path', target_path, n_iters)
    if n_iters == 0:
        # print('return', target_path)
        return len(target_path)

    subseq_paths = _unwind_directional(target_path)
    subseq_ans = solve_directional(target_path)

    assert len(subseq_paths) == len(subseq_ans)
    # for i in range(len(subseq_ans)):
    #     mine = ''.join(subseq_paths[i][0])
    #     ans = subseq_ans[i][0]
    #     if mine != ans:
    #         print(mine, ans, target_path)

    total_len = 0
    for chunk in subseq_paths:
        tmp = float('inf')
        for seq in chunk:
            res = unwind_robot(tuple(seq), n_iters-1)
            # print(res, tmp)
            if res < tmp:
                tmp = res
        total_len += tmp
        # total_len += min([unwind_robot(seq, n_iters-1) for seq in chunk])

    return total_len


def part2(codes: list[str], n_iters) -> int:
    input_lens = {}
    for code in codes:
        code_path = []
        start = 'A'
        for entry in code:
            path = _find_shortest_path(1, start, entry)
            start = entry
            code_path.append(path)

        # now we have to get the button presses that will return the above
        target_path = code_path
        target_len = 0
        for chunk in target_path:
            target_len += min([unwind_robot(tuple(seq), n_iters) for seq in chunk])

        input_lens[code] = target_len

        # # now we have to get the button presses that will return the above
        # target_path = code_path
        # target_path = unwind_robot(tuple(target_path), n_iters)

        # input_lens[code] = target_path

    complexity = 0
    for k, v in input_lens.items():
        # print(k, v)
        k_int = int(k.split('A')[0])
        complexity += k_int * v

    return complexity


if __name__ == '__main__':
    with open('advent_of_code/2024/day21/input.txt', 'r') as f:
        codes = f.readlines()
    codes = [c.strip() for c in codes]

    s = time.time()
    print(f'Complexity of codes: {part1(codes)} in {time.time() - s}')
    s = time.time()

    iters = 25
    print(f'Complexity of codes (n={iters}): {part2(codes, iters)} in {time.time() - s}')
