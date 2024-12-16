"""
Advent of Code 2024: Day 15
"""


# pylint: disable=redefined-outer-name
def part1(warehouse_map: list[list[str]], move_list: list[str]) -> int:
    """
    Given a map of the warehouse and a move list for the robot, return the final
    GPS coordinates of the boxes after completing all moves.
    Robot moves per instruction _unless_ there is a wall (# char) barrier.
    If there is a box (O) the robot moves the box in the direction of its travel.
    Need to check if any empty spaces are in the movement vector of the robot
    If the robot is unable to move, the instruction is skipped

    Args:
        warehouse_map (list[list[str]]): map with O boxes, # walls, @ robot
        move_list (list[str]): move instructions for robot

    Returns:
        int: sum of y*100 + x positions of boxes in the warehouse
    """
    move_dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    robot_pos = next(
        (i, j) for i, row in enumerate(warehouse_map) for j, c in enumerate(row) if c == '@'
    )

    assert len(robot_pos) > 0

    def _move_robot(warehouse_map, robot_pos, i, j):
        """Update robot position in grid."""
        warehouse_map[i][j] = '@'
        warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
        return (i, j)

    # iterate through the move list
    while move_list:
        move = move_list.pop(0)
        dir_i, dir_j = move_dirs[move]
        i, j = robot_pos[0] + dir_i, robot_pos[1] + dir_j
        if warehouse_map[i][j] == '.': # move robot into empty cell
            robot_pos = _move_robot(warehouse_map, robot_pos, i, j)
        elif warehouse_map[i][j] == 'O':
            # move the box along the dir
            # if multiple consecutive boxes, move all
            i_new, j_new = i + dir_i, j + dir_j
            # iterate down the row or col until first blank space or wall
            reassigns = []
            while 0 < i_new < len(warehouse_map) and 0 < j_new < len(warehouse_map[0]):
                if warehouse_map[i_new][j_new] == 'O':
                    reassigns.append((i_new, j_new))
                    i_new, j_new = i_new + dir_i, j_new + dir_j
                if warehouse_map[i_new][j_new] == '.':
                    reassigns.append((i_new, j_new))
                    break # out of the loop and move the boxes over
                if warehouse_map[i_new][j_new] == '#':
                    reassigns = [] # all boxes in a row against the wall
                    break
            if reassigns:
                warehouse_map[i_new][j_new] = 'O' # new blank spot is a robot
                robot_pos = _move_robot(warehouse_map, robot_pos, i, j)

    gps_coords = sum(
        100 * i + j
        for i, row in enumerate(warehouse_map)
        for j, c in enumerate(row) if c == 'O'
    )

    return gps_coords


# pylint: disable=redefined-outer-name
def part2(warehouse_map: list[list[str]], move_list = list[str]) -> int:
    """
    Return GPS coordinates for double wide boxes and warehouse.
    """
    move_dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    box_edge_pairs = {'[': ']', ']': '['}
    robot_pos = next(
        (i, j) for i, row in enumerate(warehouse_map) for j, c in enumerate(row) if c == '@'
    )

    assert len(robot_pos) > 0

    def _move_robot(warehouse_map, robot_pos, i, j):
        """Update robot position in grid."""
        warehouse_map[i][j] = '@'
        warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
        return (i, j)

    def _move_horizontal(warehouse_map, i, j, dir_j):
        """Evaluate box moves across row. Simple push."""
        j_new = j + dir_j
        reassigns = []
        while 0 < j_new < len(warehouse_map[0]):
            if warehouse_map[i][j_new] == '.':
                reassigns.append((i, j_new))
                break # out of the loop and move the boxes over
            if warehouse_map[i][j_new] == '#':
                reassigns = [] # all boxes in a row against the wall
                break
            if warehouse_map[i][j_new] in box_edge_pairs:
                reassigns.append((i, j_new))
                j_new += dir_j

        if not reassigns:
            return None

        for ri, rj in reassigns:
            if warehouse_map[ri][rj] == '.':
                warehouse_map[ri][rj] = box_edge_pairs[warehouse_map[i][j]]
            else:
                warehouse_map[ri][rj] = box_edge_pairs[warehouse_map[ri][rj]]
        return _move_robot(warehouse_map, robot_pos, i, j)

    def _move_vertical(warehouse_map, i, j, dir_i):
        """
        Evaluate box move vertically. Since boxes are wide, can create branches.
        
        Now moving up and down which needs to check edge alignment.
        If edges align, don't need to go adjacent, but do need to track.
        """
        j_l, j_r = j - 1, j
        if warehouse_map[i][j] == '[':
            j_l, j_r = j, j + 1

        i_new = i + dir_i
        reassigns = [(i, (j_l, j_r))]

        while -1 < i_new < len(warehouse_map):
            row_slice = warehouse_map[i_new][j_l:j_r+1]
            # row has a wall
            if '#' in row_slice: # hit a wall
                reassigns = []
                break
            # row is empty
            if all(c == '.' for c in row_slice):
                reassigns.append((i_new, (j_l, j_r)))
                break
            # row has a box
            reassigns.append((i_new, (j_l, j_r)))
            if warehouse_map[i_new][j_l] == ']': # expands
                j_l -= 1
            elif warehouse_map[i_new][j_l] == '.': # contracted
                j_l += warehouse_map[i_new][j_l:].index('[')
            if warehouse_map[i_new][j_r] == '[': # expands
                j_r += 1
            elif warehouse_map[i_new][j_r] == '.': # contracted
                substr = ''.join(warehouse_map[i_new][:j_r])
                j_r -= len(substr) - substr.rindex(']')

            i_new = i_new + dir_i

        if not reassigns:
            return None

        for (ti, (tj_l, tj_r)), (si, _) in zip(reversed(reassigns), reversed(reassigns[:-1])):
            for idx in range(tj_l, tj_r + 1):
                if warehouse_map[si][idx] in box_edge_pairs:
                    warehouse_map[ti][idx] = warehouse_map[si][idx]
                    warehouse_map[si][idx] = '.'
        return _move_robot(warehouse_map, robot_pos, i, j)

    while move_list:
        move = move_list.pop(0)
        dir_i, dir_j = move_dirs[move]
        i, j = robot_pos[0] + dir_i, robot_pos[1] + dir_j
        if warehouse_map[i][j] == '.': # move robot into empty cell
            robot_pos = _move_robot(warehouse_map, robot_pos, i, j)
        elif warehouse_map[i][j] in box_edge_pairs:
            # since boxes are now two spaces wide, they can create trees
            # need to iterate down both halves of the box and check for next cell
            if move in ['<', '>']:
                if result := _move_horizontal(warehouse_map, i, j, dir_j):
                    robot_pos = result
            else:
                if result := _move_vertical(warehouse_map, i, j, dir_i):
                    robot_pos = result

    gps_coords = sum(
        100 * i + j
        for i, row in enumerate(warehouse_map)
        for j, c in enumerate(row) if c == '['
    )

    return gps_coords


if __name__ == '__main__':
    raw_warehouse = []
    robot_moves = []
    tgt_list = raw_warehouse
    with open('advent_of_code/2024/day15/input.txt', 'r') as f:
        for l in f.readlines():
            if l == '\n':
                tgt_list = robot_moves
                continue
            tgt_list.append(l.strip())

    robot_moves = [i for sublist in robot_moves for i in sublist]
    warehouse_map = [list(l) for l in raw_warehouse]

    print(f'GPS of all boxes: {part1(warehouse_map, robot_moves.copy())}')

    WAREHOUSE_STR = '\n'.join(raw_warehouse).replace('#', '##')\
                        .replace('O', '[]')\
                        .replace('.', '..')\
                        .replace('@', '@.')
    wide_warehouse = WAREHOUSE_STR.split('\n')
    wide_warehouse = [list(l) for l in wide_warehouse]
    assert len(wide_warehouse[0]) == 2 * len(warehouse_map[0])

    print(f'GPS of wide boxes: {part2(wide_warehouse, robot_moves.copy())}')
