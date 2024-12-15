"""
Advent of Code 2024: Day 15
"""


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
    # find initial grid position of robot
    robot_pos = ()
    for i, row in enumerate(warehouse_map):
        for j, c in enumerate(row):
            if c == '@':
                robot_pos = (i, j)

    assert len(robot_pos) > 0

    # iterate through the move list
    while move_list:
        move = move_list.pop(0)
        direc = move_dirs[move]
        i, j = robot_pos[0] + direc[0], robot_pos[1] + direc[1]
        if warehouse_map[i][j] == '.': # move robot into empty cell
            warehouse_map[i][j] = '@'
            warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
            robot_pos = (i, j)
        elif warehouse_map[i][j] == 'O':
            # move the box along the dir
            # if multiple consecutive boxes, move all
            i2, j2 = i + direc[0], j+direc[1]
            # iterate down the row or col until first blank space or wall
            reassigns = []
            while 0 < i2 < len(warehouse_map) and 0 < j2 < len(warehouse_map[0]):
                if warehouse_map[i2][j2] == 'O':
                    reassigns.append((i2, j2))
                    i2, j2 = i2 + direc[0], j2 + direc[1]
                if warehouse_map[i2][j2] == '.':
                    reassigns.append((i2, j2))
                    break # out of the loop and move the boxes over
                elif warehouse_map[i2][j2] == '#':
                    reassigns = [] # all boxes in a row against the wall
                    break
            if reassigns:
                warehouse_map[i2][j2] = 'O' # new blank spot is a robot
                warehouse_map[i][j] = '@'
                warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
                robot_pos = (i, j)

    gps_coords = 0
    for i, row in enumerate(warehouse_map):
        for j, c in enumerate(row):
            if c == 'O':
                gps_coords += 100 * i + j

    return gps_coords


def part2(warehouse_map: list[list[str]], move_list = list[str]) -> int:
    """
    Return GPS coordinates for double wide boxes and warehouse.
    """
    move_dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    box_edge_pairs = {'[': ']', ']': '['}
    # find initial grid position of robot
    robot_pos = ()
    for i, row in enumerate(warehouse_map):
        for j, c in enumerate(row):
            if c == '@':
                robot_pos = (i, j)

    assert len(robot_pos) > 0

    # iterate through the move list
    n_move = 0
    while move_list:
        n_move += 1
        move = move_list.pop(0)
        direc = move_dirs[move]
        i, j = robot_pos[0] + direc[0], robot_pos[1] + direc[1]
        if warehouse_map[i][j] == '.': # move robot into empty cell
            warehouse_map[i][j] = '@'
            warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
            robot_pos = (i, j)
        elif warehouse_map[i][j] in ['[', ']']:
            # since boxes are now two spaces wide, they can create trees
            # need to iterate down both halves of the box and check for next cell
            # the horizontal move case is largely the same as part1
            if move in ['<', '>']:
                i2, j2 = i + direc[0], j+direc[1]
                reassigns = []
                while 0 < i2 < len(warehouse_map) and 0 < j2 < len(warehouse_map[0]):
                    if warehouse_map[i2][j2] in ['[', ']']:
                        reassigns.append((i2, j2))
                        i2, j2 = i2 + direc[0], j2 + direc[1]
                    if warehouse_map[i2][j2] == '.':
                        reassigns.append((i2, j2))
                        break # out of the loop and move the boxes over
                    elif warehouse_map[i2][j2] == '#':
                        reassigns = [] # all boxes in a row against the wall
                        break
                if reassigns:
                    for ri, rj in reassigns:
                        if warehouse_map[ri][rj] == '.':
                            warehouse_map[ri][rj] = box_edge_pairs[warehouse_map[i][j]]
                        else:
                            warehouse_map[ri][rj] = box_edge_pairs[warehouse_map[ri][rj]]
                    warehouse_map[i][j] = '@'
                    warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
                    robot_pos = (i, j)
            else:
                # now moving up and down which needs to check edge alignment
                # if edges align, don't need to go adjacent, but do need to track
                # as soon a wall is hit anywhere in the wide edge of the box tree, stop
                if warehouse_map[i][j] == '[':
                    j_l, j_r = j, j+1
                else:
                    j_l, j_r = j-1, j
                i2 = i + direc[0]
                reassigns = [(i, (j_l, j_r))]
                while -1 < i2 < len(warehouse_map):
                    box_pyramid_width = j_r+1 - j_l
                    # row has a wall
                    if '#' in warehouse_map[i2][j_l:j_r+1]: # hit a wall
                        reassigns = []
                        break
                    # row is empty
                    if warehouse_map[i2][j_l:j_r+1] == ['.'] * box_pyramid_width:
                        reassigns.append((i2, (j_l, j_r)))
                        break
                    # row has a box
                    else:
                        reassigns.append((i2, (j_l, j_r)))
                        if warehouse_map[i2][j_l] == ']': # expands
                            j_l -= 1
                        elif warehouse_map[i2][j_l] == '.': # contracted
                            j_l += warehouse_map[i2][j_l:].index('[')
                        if warehouse_map[i2][j_r] == '[': # expands
                            j_r += 1
                        elif warehouse_map[i2][j_r] == '.': # contracted
                            substr = ''.join(warehouse_map[i2][:j_r])
                            j_r -= len(substr) - substr.rindex(']')

                    i2 = i2 + direc[0]
                if reassigns:
                    # starting at the end, move the boxes to the new empty spaces
                    for ri in range(-1, -len(reassigns), -1):
                        ti, tj = reassigns[ri]
                        si, sj = reassigns[ri-1]

                        # move cells from source to target that make up the relevant boxes
                        # we _only_ want to move boxes, not empty spaces
                        for copy_idx in range(tj[0],tj[1]+1):
                            if warehouse_map[si][copy_idx] in ['[', ']']:
                                warehouse_map[ti][copy_idx] = warehouse_map[si][copy_idx]
                                warehouse_map[si][copy_idx] = '.'
                    warehouse_map[i][j] = '@'
                    warehouse_map[robot_pos[0]][robot_pos[1]] = '.'
                    robot_pos = (i, j)

    gps_coords = 0
    for i, row in enumerate(warehouse_map):
        for j, c in enumerate(row):
            if c == '[':
                gps_coords += 100 * i + j

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

    warehouse_str = '\n'.join(raw_warehouse).replace('#', '##')\
                        .replace('O', '[]')\
                        .replace('.', '..')\
                        .replace('@', '@.')
    wide_warehouse = warehouse_str.split('\n')
    wide_warehouse = [list(l) for l in wide_warehouse]
    assert len(wide_warehouse[0]) == 2 * len(warehouse_map[0])

    print(f'GPS of wide boxes: {part2(wide_warehouse, robot_moves.copy())}')
