"""
Advent of Code 2024: Day 16
"""
import heapq


def maze_to_graph(maze, include_interm=False):
    n_rows, n_cols = len(maze), len(maze[0])
    graph = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def _is_walkable(i, j):
        return 0 <= i < n_rows and 0 <= j < n_cols and maze[i][j] in '.SE'

    def _is_node(i, j):
        if not _is_walkable(i, j):
            return False

        # nodes will either terminate with deadend (no path neighbors) or they
        # are at a fork within the maze (two neighbors with paths)
        neighbors = []
        for di, dj in directions:
            if _is_walkable(i + di, j + dj):
                neighbors.append((di, dj))

        if len(neighbors) != 2:
            return True

        # check for a corner or straight line
        return neighbors[0][0] != neighbors[1][0] and neighbors[0][1] != neighbors[1][1]


    for i in range(n_rows):
        for j in range(n_cols):
            if (include_interm and maze[i][j] != '#') or _is_node(i, j):
                graph[(i, j)] = {}

                for di, dj in directions:
                    i_new, j_new = i + di, j + dj
                    path_len = 0
                    while _is_walkable(i_new, j_new):
                        path_len += 1
                        # if only_terminal and _is_node(i_new, j_new):
                        if not include_interm:
                            if _is_node(i_new, j_new):
                                graph[(i, j)][(i_new, j_new)] = path_len
                                break
                            # else:
                                # graph[(i, j)][(i_new, j_new)] = path_len
                            i_new += di
                            j_new += dj
                        else:
                            graph[(i, j)][(i_new, j_new)] = path_len
                            break

    return graph


class Node:
    def __init__(self, coords):
        self.dist = float('inf')
        self.parent = None
        self.visited = False
        self.coords = coords
        self.travel_dir = None
        self.paths = []


def part1(maze) -> int:
    # traverse the graph from S to E in shortest distance
    # + 1000 for each turn and +1 for each square
    # start facing east

    graph = maze_to_graph(maze)
    start_node = next(
        (i, j) for i, row in enumerate(maze) for j, c in enumerate(row) if c == 'S'
    )
    exit_node = next(
        (i, j) for i, row in enumerate(maze) for j, c in enumerate(row) if c == 'E'
    )

    nodes = {}
    for node in graph:
        nodes[node] = Node(node)
    nodes[start_node].dist = 0
    nodes[start_node].travel_dir = (0, 1)

    pq = [(0, start_node)]

    while pq:
        dist, node = heapq.heappop(pq)
        if nodes[node].visited:
            continue
        nodes[node].visited = True
        for neighbor in graph[node]:
            if nodes[neighbor].visited:
                continue
            # check for new distance which needs to verify if a turn was made
            new_dist = dist + graph[node][neighbor]
            if nodes[node].parent:
                # check straight line
                parent = nodes[node].parent
                i_parent, j_parent = nodes[parent].coords
                if not (i_parent == neighbor[0] or j_parent == neighbor[1]):
                    new_dist += 1000
            else: # start node is parent node
                i_offset, j_offset = nodes[start_node].travel_dir
                i_parent, j_parent = start_node[0] + i_offset, start_node[1] + j_offset
                if not (i_parent == neighbor[0] or j_parent == neighbor[1]):
                    new_dist += 1000
            if new_dist < nodes[neighbor].dist:
                nodes[neighbor].dist = new_dist
                nodes[neighbor].parent = node
                heapq.heappush(pq, (new_dist, neighbor))

    return nodes[exit_node].dist


def part2(maze) -> int:
    graph = maze_to_graph(maze, include_interm=True)
    start_node = next(
        (i, j) for i, row in enumerate(maze) for j, c in enumerate(row) if c == 'S'
    )
    exit_node = next(
        (i, j) for i, row in enumerate(maze) for j, c in enumerate(row) if c == 'E'
    )

    queue = [[start_node]]
    paths = []

    while queue:
        path = queue.pop()
        current_node = path[-1]

        if current_node == exit_node:
            paths.append(path)
            continue

        for neighbor in graph[current_node]:
            if neighbor not in path:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    best_score = float('inf')
    best_paths = []
    for path in paths:
        path_score = 0
        prev = path[0]
        prev_dir = (0, 1)
        # calculate score
        for curr in path[1:]:
            di, dj = curr[0] - prev[0], curr[1] - prev[1]
            if di != 0:
                path_score += abs(di)
                di /= abs(di)
            if dj != 0:
                path_score += abs(dj)
                dj /= abs(dj)
            if (di, dj) != prev_dir:
                path_score += 1000
            prev_dir = (di, dj)
            prev = curr
        if path_score < best_score:
            best_score = path_score
            best_paths = [path]
        elif path_score == best_score:
            best_paths.append(path)

    return len(set().union(*best_paths))


if __name__ == '__main__':
    with open('advent_of_code/2024/day16/input.txt', 'r') as f:
        raw_maze = f.readlines()
    raw_maze = [l.strip() for l in raw_maze]

    print(f'Lowest score possible: {part1(raw_maze)}')
    print(f'Number of seats: {part2(raw_maze)}')
