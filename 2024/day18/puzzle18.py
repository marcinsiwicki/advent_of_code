"""
Advent of Code 2024: Day 18
RAM Run
"""
import heapq


MODE = 'PROD'
if MODE == 'PROD':
    N_BYTES_SIM = 1024
    N_GRID = 70 + 1
    FILENAME = 'input.txt'
else:
    N_BYTES_SIM = 12
    N_GRID = 7
    FILENAME = 'test.txt'


def _in_bounds(node, maze_grid, maze_size):
    """Helper function to determine if in bounds or wall."""
    i, j = node
    if i < 0 or i >= maze_size:
        return False
    if j < 0 or j >= maze_size:
        return False
    if maze_grid[i][j] == '#':
        return False
    return True


def part1(falling_bytes: list[tuple[int]]) -> tuple[int, list[list[str]]]:
    """
    Given a list of falling bytes, create grid and find shortest path to
    exit node.

    Args:
        falling_bytes (list[tuple[int]]): items that appear on grid to block

    Returns:
        tuple[int, list[list[str]]]: returns shortest path len and grid state
    """

    maze_grid = [['.' for _ in range(N_GRID)] for _ in range(N_GRID)]
    directions = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    for x, y in falling_bytes[:N_BYTES_SIM]:
        maze_grid[y][x] = '#'

    start_node = (N_GRID - 1, N_GRID - 1)
    exit_node = (0, 0)
    visited = set()
    distances = {start_node: 0}

    pq = [(0, (start_node))]

    while pq:
        dist, node = heapq.heappop(pq)
        # see if we can advance in a given direction without hitting a wall
        if node in visited:
            continue
        visited.add(node)
        for di, dj in directions:
            neighbor = (node[0] + di, node[1] + dj)
            if not _in_bounds(neighbor, maze_grid, N_GRID):
                continue
            if neighbor not in distances:
                distances[neighbor] = float('inf')
            new_dist = dist + 1
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq ,(new_dist, neighbor))

    return distances[exit_node], maze_grid


def part2(falling_bytes, maze_grid):
    """
    Given a grid state and remainding bytes, find first instance where a 
    path to the exit cannot be found.
    """
    # from here on out, we need to drop a byte in and verify if there is
    # still a path to the exit. if not we return that byte
    directions = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    start = (N_GRID - 1, N_GRID - 1)
    exit = (0, 0)

    for x, y in falling_bytes[N_BYTES_SIM:]:
        maze_grid[y][x] = '#'

        visited = set()
        distances = {start: 0}
        pq = [(0, (start))]

        while pq:
            dist, node = heapq.heappop(pq)
            # see if we can advance in a given direction without hitting a wall
            if node in visited:
                continue
            visited.add(node)
            for di, dj in directions:
                neighbor = (node[0] + di, node[1] + dj)
                if not _in_bounds(neighbor, maze_grid, N_GRID):
                    continue
                if neighbor not in distances:
                    distances[neighbor] = float('inf')
                new_dist = dist + 1
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq ,(new_dist, neighbor))
        if exit not in distances:
            return x, y

    return (-1, -1)


if __name__ == '__main__':
    with open(f'advent_of_code/2024/day18/{FILENAME}', 'r') as f:
        falling_bytes = f.readlines()
    falling_bytes = [(int(l.split(',')[0]), int(l.split(',')[1])) for l in falling_bytes]

    shortest_path, maze_state = part1(falling_bytes)
    print(f'Shortest path: {shortest_path}')
    print(f'Path ends with: {part2(falling_bytes, maze_state)}')
