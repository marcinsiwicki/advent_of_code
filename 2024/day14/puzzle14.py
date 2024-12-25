"""
Advent of Code 2024: Day 14
Restroom Redoubt
"""
import pprint
import numpy as np


MODE = 'PROD'
PUZZLE_PARAMS = {'DEBUG': {'file': 'test.txt', 'height': 7, 'width': 11},
                 'PROD': {'file': 'input.txt', 'height': 103, 'width': 101}}


def part1(robots: list[list[tuple]], n_seconds: int = 100) -> int:
    """
    Predict position of robots after n_seconds depending on their initial pos and velocity.
    Assign them to a quadrant and return overall safety score.

    Args:
        robots (list[list[tuple]]): robots represented by a tuple for init pos and for velocity
        n_seconds (int, optional): number of seconds to observe before scoring. Defaults to 100.

    Returns:
        int: return product of each quadrants sum of robots
    """
    # we can extrapolate each robot to its final position in an unconstrained grid
    # then work backwards and determine how many wraps are needed to adjust to the final pos
    quadrant_scores = [[0, 0], [0, 0]]

    n_width = PUZZLE_PARAMS[MODE]['width']
    n_height = PUZZLE_PARAMS[MODE]['height']
    width_part, height_part = n_width // 2, n_height // 2

    for robot in robots:
        ipos_x, ipos_y = robot[0]
        vel_x, vel_y = robot[1]

        fpos_x = (ipos_x + vel_x * n_seconds) % n_width
        fpos_y = (ipos_y + vel_y * n_seconds) % n_height

        if fpos_x == width_part or fpos_y == height_part:
            continue
        qpos_x = int(fpos_x < width_part)
        qpos_y = int(fpos_y < height_part)
        quadrant_scores[qpos_x][qpos_y] += 1

    product = 1
    for s in quadrant_scores[0] + quadrant_scores[1]:
        product *= s

    return product


def part2(robots: list[list[tuple]]) -> int:
    """
    Find when the robots assemble into a tree.

    Args:
        robots (list[list[tuple]]): list of robot pos and vectors

    Returns:
        int: number of seconds until they assemble into shape
    """
    n_width = PUZZLE_PARAMS[MODE]['width']
    n_height = PUZZLE_PARAMS[MODE]['height']

    bx = min(range(n_width), key=lambda t: np.var([(s[0]+t*v[0]) % n_width for (s,v) in robots]))
    by = min(range(n_height), key=lambda t: np.var([(s[1]+t*v[1]) % n_height for (s,v) in robots]))

    return bx + ((pow(n_width, -1, n_height) * (by - bx)) % n_height) * n_width

#    n_robots = len(robots)
#
#    grid_entropy = []
#    for second in range(n_width * n_height):
#        # move to next grid pos per robot
#        grid_positions = []
#        for robot in robots:
#            ipos_x, ipos_y = robot[0]
#            vel_x, vel_y = robot[1]
#
#            fpos_x = (ipos_x + vel_x * second) % n_width
#            fpos_y = (ipos_y + vel_y * second) % n_width
#
#            grid_positions.append((fpos_x, fpos_y))
#
#        # calculate entropy
#        grid = np.zeros((n_width, n_height), int)
#        for pos in grid_positions:
#            np.add.at(grid, pos, 1)
#        counts = np.bincount(grid.flatten())
#        probs = counts[counts > 0] / counts.sum()
#        shannon = -np.sum(probs * np.log2(probs))
#        grid_entropy.append(shannon)
#
#    min_entropy = min(grid_entropy)
#    min_index = grid_entropy.index(min_entropy)
#
#    return min_index

#    n_seconds = 0
#    while True:
#        # populate initial grid
#        grid = [[' ' for _ in range(n_width)] for _ in range(n_height)]
#        grid_pos = []
#        for robot in robots:
#            ipos_x, ipos_y = robot[0]
#            vel_x, vel_y = robot[1]
#
#            fpos_x = (ipos_x + vel_x * n_seconds) % n_width
#            fpos_y = (ipos_y + vel_y * n_seconds) % n_width
#
#            grid_pos.append((fpos_y, fpos_x))
#            grid[fpos_y][fpos_x] = 'X'
#
#        for i in range(n_width):
#            trunk_robots = [e for e in grid_pos if e[1] == i]
#            if len(trunk_robots) > 0.25 * n_height:
#                for l in grid:
#                    print(''.join(l))
#                print('*' * n_width)
#                break
#
#        n_seconds += 1


if __name__ == '__main__':
    robot_details = []
    with open(f'advent_of_code/2024/day14/{PUZZLE_PARAMS[MODE]["file"]}', 'r') as f:
        for l in f.readlines():
            pos, vel = l.split(' ')
            xpos, ypos = pos[2:].split(',')
            xvel, yvel = vel[2:].split(',')
            robot_details.append([(int(xpos), int(ypos)), (int(xvel), int(yvel))])

    print(f'Safety score: {part1(robot_details)}')
    print(f'Seconds until tree: {part2(robot_details)}')
