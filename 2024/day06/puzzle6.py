"""
Advent of Code 2024: Day 6
"""
import time
import copy

def part1(input_maze: list) -> int:
    """Find distinct positions in patrol path."""
    guards = {'^': (-1, 0),
              '>': (0, 1),
              'v': (1, 0),
              '<': (0, -1)
    }


    def next_guard(cur_guard):
        guards_ = list(guards.keys())

        if guards_.index(cur_guard) == len(guards_) - 1:
            return guards_[0]
        return guards_[guards_.index(cur_guard) + 1]


    # identify where the guard is to start and iter dir based on view
    # once the guard is not in the grid at all, return the positions
    n_rows = len(input_maze)
    n_cols = len(input_maze[0])
    positions = set()

    check_char = '^'
    i = 0
    while i < n_rows:
        if check_char in input_maze[i]:
            j = input_maze[i].index(check_char)

            # check orientation
            offset_y, offset_x = guards[check_char]

            if -1 < (i + offset_y) < n_rows and -1 < (j + offset_x) < n_cols:
                next_loc = input_maze[i + offset_y][j + offset_x]
            else:
                input_maze[i][j] = 'X'
                break

            if next_loc != "#": # if not obstacle
                input_maze[i + offset_y][j + offset_x] = check_char
                # reset current cell
                input_maze[i][j] = 'X'
                positions.add((i, j))
                i = i + offset_y # we can now just go new guard row
            else:
                check_char = next_guard(check_char)
                input_maze[i][j] = check_char
        else:
            i += 1

    return len(positions) + 1, input_maze


def is_time_loop(new_matrix, y) -> bool:
    guards = {'^': (-1, 0),
              '>': (0, 1),
              'v': (1, 0),
              '<': (0, -1)
    }


    def next_guard(cur_guard):
        guards_ = list(guards.keys())

        if guards_.index(cur_guard) == len(guards_) - 1:
            return guards_[0]
        return guards_[guards_.index(cur_guard) + 1]


    n_rows = len(new_matrix)
    n_cols = len(new_matrix[0])

    check_char = '^'
    i = y
    first_iter = True
    known_moves = set()
    while i < n_rows:
        if check_char in new_matrix[i]:
            j = new_matrix[i].index(check_char)

            # check orientation
            offset_y, offset_x = guards[check_char]

            # leave the board
            if -1 < (i + offset_y) < n_rows and -1 < (j + offset_x) < n_cols:
                next_loc = new_matrix[i + offset_y][j + offset_x]
            else:
                new_matrix[i][j] = 'X'
                break

            if next_loc != "#": # if not obstacle
                new_matrix[i + offset_y][j + offset_x] = check_char
                # reset current cell
                new_matrix[i][j] = 'X'
                if (i, j, check_char) in known_moves:
                    return True
                known_moves.add((i, j, check_char))
                i = i + offset_y # we can now just go new guard row
            else:
                check_char = next_guard(check_char)
                new_matrix[i][j] = check_char
        else:
            i += 1

    return False


def part2(input_maze: list, known_path: list) -> int:
    """Place an obstruction to get the guard stuck in a loop."""
    # the obstacle should go on somewhere in the path
    # brute force: for each X place and see if guard still goes out or if 
    # there is a loop. a loop is defined as guard passing through the starting
    # position with the starting orientation.

    # find original pos in input_maze
    starting_orientation = '^'
    x_0, y_0 = None, None
    for i, l in enumerate(input_maze):
        if starting_orientation in l:
            x_0 = l.index(starting_orientation)
            y_0 = i
            break

    def reset_maze(in_maze):
        for i, l in enumerate(in_maze):
            for j, c in enumerate(l):
                if c in ['^', '>', 'v', '<']:
                    in_maze[i][j] = '.'
        in_maze[y_0][x_0] = '^'

    time_loops = []
    # use known path X and input_maze to traverse and see if loop is formed
    for i, l in enumerate(known_path):
        for j, c in enumerate(l):
            if c == 'X':
                # reset the maze without copying
                reset_maze(input_maze)
                input_maze[i][j] = '#'
                time_loops.append(is_time_loop(input_maze, y_0))
                input_maze[i][j] = 'X'

    return sum(time_loops)


if __name__ == '__main__':
    with open('advent_of_code/2024/day06/input.txt', 'r') as f:
        maze = f.readlines()

    # convert maze to matrix
    maze = [list(l.strip()) for l in maze]

    positions, traversed = part1(copy.deepcopy(maze))
    print(f'Guard positions: {positions}')
    b = time.time()
    print(f'Possible loops: {part2(maze, traversed)}')
    print(time.time() - b)
