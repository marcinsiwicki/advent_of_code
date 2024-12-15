import itertools
import typing

# type Map = list[list[str]]
# type Coord = tuple[int, int]
# type Swap = tuple[int, int, int, int]

move_dict = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def read_input():
    map = []
    moves = []
    with open("advent_of_code/2024/day15/input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                break
            map.append(list(line))

        for line in f:
            moves += [move_dict[m] for m in line.strip()]

    return map, moves


def show(map):
    print("    " + "".join(str(i % 10) for i in range(len(map[0]))))
    for y, row in enumerate(map):
        print(f"{y:3} " + "".join(row))
    print()


def gps(map):
    for y, row in enumerate(map):
        for x, block in enumerate(row):
            if block in "O[":
                yield y * 100 + x


def robo_pos(map):
    for y, row in enumerate(map):
        if "@" in row:
            return row.index("@"), y
    raise Exception("No robot found")


def transform_map(map):
    d = {
        "#": ["#", "#"],
        ".": [".", "."],
        "O": ["[", "]"],
        "@": ["@", "."],
    }
    return [list(itertools.chain.from_iterable(d[block] for block in row)) for row in map]


def make_moves(map, moves) -> None:
    done = set()
    for x1, y1, x2, y2 in moves:
        if (x1, y1, x2, y2) not in done:
            map[y2][x2], map[y1][x1] = map[y1][x1], map[y2][x2]
            done.add((x1, y1, x2, y2))


def get_moves(map, x: int, y: int, dx: int, dy: int):
    """Can we move from x,y to x+dx, y+dy?
    If so, return moveslist as items to be swapped, ordered from first to last swap
    to make.
    NOTE: swaps not neccessarily unique
    Eg. pushing up on two boxes on top of each other has each part pushing both sides of the
    top box, resulting in the same swap being made twice.
    This needs to be filtered out by make_moves or ends up swapping twice
    """
    x2, y2 = x + dx, y + dy  # Square moving into.
    block = map[y2][x2]

    cur_move = [(x, y, x2, y2)]

    if block == ".":
        return cur_move

    elif block == "#":
        return None
    elif block in "[]":
        neighbour_x = x2 + 1 if block == "[" else x2 - 1

        move1 = get_moves(map, x2, y2, dx, dy)
        if move1 is None:
            return None
        if dy:
            move2 = get_moves(map, neighbour_x, y2, dx, dy)
            if move2 is not None:
                return move1 + move2 + cur_move
        else:
            return move1 + cur_move
    elif block == "O":
        move1 = get_moves(map, x2, y2, dx, dy)
        if move1 is None:
            return None
        return move1 + cur_move
    else:
        raise Exception(f"Invalid block: {block}")


def solve(map, moves) -> int:
    rx, ry = robo_pos(map)
    assert map[ry][rx] == "@"

    i = 1
    interim_res = []
    assert len(moves) == 20000
    for dx, dy in moves:
        cur_moves = get_moves(map, rx, ry, dx, dy)
        if cur_moves:
            make_moves(map, cur_moves)
            rx += dx
            ry += dy
        if i in (4354, 4355, 4356):
            show(map)
        # interim_res.append((i, sum(gps(map))))
        i += 1
        
    show(map)

    # with open('advent_of_code/2024/day15/interim.txt', 'w') as f:
        # for l in interim_res:
            # f.write(f'{l[0]}: {l[1]}\n') 
    
    return sum(gps(map))


map, moves = read_input()
map2 = transform_map(map)
print(solve(map, moves))
print(solve(map2, moves))
