""" Advent of Code 2024: Day 20 Race Condition """
from collections import defaultdict


def part1(racetrack: list[list[str]]) -> int:
    """Given a racetrack, find the path through and then check for possible shortcuts."""

    # find the intial set of tiles that get you through the racetrack
    start = next(
        (i, j) for i, row in enumerate(racetrack) for j, c in enumerate(row) if c == 'S'
    )
    end = next(
        (i, j) for i, row in enumerate(racetrack) for j, c in enumerate(row) if c == 'E'
    )

    exit_path = [start] # tiles accessed to get to end
    directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
    prev_dir = (0, 0)

    i, j = start
    while (i, j) != end:
        for di, dj in directions - {prev_dir}:
            i_next, j_next = i + di, j + dj
            if racetrack[i_next][j_next] == '#':
                continue
            else:
                prev_dir = (-di, -dj)
                i, j = i_next, j_next
                exit_path.append((i, j))
                break

    cheat_paths = {}
    for lead_idx, lead in enumerate(exit_path):
        for lag in exit_path[lead_idx + 1:]:
            # teleportation is possible iff i or j diff is 2 and wall in between
            i_1, j_1 = lead
            i_2, j_2 = lag
            vert_shift = abs(i_2 - i_1) == 2 and abs(j_2 - j_1) == 0
            horz_shift = abs(i_2 - i_1) == 0 and abs(j_2 - j_1) == 2
            i_btw, j_btw = (i_1 + i_2) // 2, (j_1 + j_2) // 2

            if (vert_shift or horz_shift) and racetrack[i_btw][j_btw] == '#':
                dist_skipped = (exit_path.index(lag) - exit_path.index(lead)) - 2
                cheat_paths[(lead, lag)] = dist_skipped

    return sum(1 for k, v in cheat_paths.items() if v >= 100), exit_path


def part2_hard(racetrack: list[list[str]]) -> int:
    """
    The idea here was to only move through a valid cheat if all points in the cheat were wall
    and not wall + open space.
    """

    tile_to_wall = defaultdict(list)
    wall_to_tile = defaultdict(list)

    # cheats need to have solid wall between entry and exit
    # for each wall loc - find other accessible wall locs
    start = next(
        (i, j) for i, row in enumerate(racetrack) for j, c in enumerate(row) if c == 'S'
    )
    end = next(
        (i, j) for i, row in enumerate(racetrack) for j, c in enumerate(row) if c == 'E'
    )

    n_rows, n_cols = len(racetrack), len(racetrack[0])

    exit_path = [start] # tiles accessed to get to end
    directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
    prev_dir = (0, 0)

    i, j = start
    while (i, j) != end:
        for di, dj in directions:
            i_next, j_next = i + di, j + dj
            if racetrack[i_next][j_next] == '#':
                # if 0 < i_next < n_rows-1 and 0 < j_next < n_cols-1:
                wall_to_tile[(i_next, j_next)].append((i, j))
                tile_to_wall[(i, j)].append((i_next, j_next))
            elif (di, dj) != prev_dir:
                prev_dir = (-di, -dj)
                i, j = i_next, j_next
                exit_path.append((i, j))

    # build out wall clusters
    wall_clusters = [set()]
    wall_tiles = []
    for i, row in enumerate(racetrack):
        for j, c in enumerate(row):
            if c == '#': # and (0 < i < n_rows-1) and (0 < j < n_cols-1):
                wall_tiles.append((i, j))

    def _adjacent(tile, cluster):
        for adj in cluster:
            if abs(adj[0] - tile[0]) == 1 and (adj[1] == tile[1]):
                return True
            if abs(adj[1] - tile[1]) == 1 and (adj[0] == tile[0]):
                return True
        return False

    while wall_tiles:
        tile = wall_tiles.pop(0)
        added = False
        for cluster in wall_clusters:
            if added := _adjacent(tile, cluster):
                cluster.add(tile)
        if not added:
            wall_clusters.append(set([tile]))

    # consolidate wall clusters if possible
    for i in range(len(wall_clusters)):
        for j in range(len(wall_clusters)):
            if i == j:
                continue
            if len(wall_clusters[i] & wall_clusters[j]) > 0:
                wall_clusters[i] |= wall_clusters[j]
                wall_clusters[j] = set()
    wall_clusters = [c for c in wall_clusters if c]

    wall_cluster_map = {}
    for wall in wall_to_tile:
        for i, cluster in enumerate(wall_clusters):
            if wall in cluster:
                wall_cluster_map[wall] = i

    cheat_paths = {}
    for lead_idx, lead in enumerate(exit_path):
        c_lead = complex(*lead)
        for wall in tile_to_wall[lead]:
            cluster = wall_clusters[wall_cluster_map[wall]]
            for adj_wall in cluster:
                if adj_wall == wall:
                    continue
                cheat_exits = wall_to_tile[adj_wall]
                for lag in cheat_exits:
                    c_lag = complex(*lag)
                    dist = c_lag - c_lead
                    dist = int(abs(dist.real) + abs(dist.imag)) # number of picos cheat takes
                    if dist <= 20:
                        dist_skipped = (exit_path.index(lag) - exit_path.index(lead))
                        dist_skipped -= dist
                        if dist_skipped > 0:
                            cheat_paths[(lead, lag)] = dist_skipped

    return sum(1 for k, v in cheat_paths.items() if v >= 100)


def part2(racetrack, exit_path):
    cheat_paths = {}
    for i in range(len(exit_path)):
        for j in range(i+1, len(exit_path)):
            lead = exit_path[i]
            lag = exit_path[j]

            dist = abs(lag[0] - lead[0]) + abs(lag[1] - lead[1])

            if dist <= 20:
                dist_skipped = j - i - dist
                cheat_paths[(lead, lag)] = dist_skipped

    return sum(1 for k, v in cheat_paths.items() if v >= 100)


if __name__ == '__main__':
    with open('advent_of_code/2024/day20/input.txt', 'r') as f:
        racetrack = f.read().split('\n')
    racetrack = [list(l) for l in racetrack]
    cheat_count, exit_path = part1(racetrack)
    print(f'Cheating paths > 100 picos: {cheat_count}')
    print(f'Longer cheat window paths: {part2(racetrack, exit_path)}')
