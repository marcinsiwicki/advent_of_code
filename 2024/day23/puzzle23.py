"""
Advent of Code 2024: Day 23
LAN Party
"""
from itertools import combinations


def _build_lan_map(computer_links: list[tuple[str]]):
    lan_map = {}
    for c1, c2 in computer_links:
        if c1 in lan_map:
            lan_map[c1].add(c2)
        else:
            lan_map[c1] = {c2}
        if c2 in lan_map:
            lan_map[c2].add(c1)
        else:
            lan_map[c2] = {c1}
    return lan_map


def part1(computer_links: list[tuple[str]]) -> int:
    """
    Return number of possible trios with leading `t` char.
    Each item in the input represents a birectional link of two computers.
    We want to identify all clusters of three connected machines
      can brute force by getting all unique comps, finding what they're connected
      to - and then seeing if those are connected with each other
    """

    lan_map = _build_lan_map(computer_links)
    possible_trios = set()
    # iterate through dict and check all combinations of pairs to see if they
    # contain each other
    for k, v in lan_map.items():
        iter_comps = list(combinations(v, 2))
        for c1, c2 in iter_comps:
            if c1 in lan_map[c2] and c2 in lan_map[c1]:
                possible_trios.add(tuple(sorted([k, c1, c2])))

    sets_with_t = 0
    for trio in possible_trios:
        if any(s.startswith('t') for s in trio):
            sets_with_t += 1

    return sets_with_t


def part2(computer_links: list[tuple[str]]) -> int:
    """Find maximum clique within graph of computers."""
    # need to find largest cluster of connected computers
    lan_map = _build_lan_map(computer_links)

    def _bron_kerbosch(R, P, X, G):
        if not P and not X:
            yield R
        for v in P.copy():
            R_new = R | {v}
            P_new = P & G[v]
            X_new = X & G[v]
            yield from _bron_kerbosch(R_new, P_new, X_new, G)
            P.remove(v)
            X.add(v)

    cliques = list(_bron_kerbosch(set(), set(lan_map.keys()), set(), lan_map))
    max_clique = max(cliques, key=len)

    return ','.join(sorted(max_clique))


if __name__ == '__main__':
    with open('advent_of_code/2024/day23/input.txt', 'r') as f:
        computer_links = f.readlines()
    computer_links = [tuple(i.strip().split('-')) for i in computer_links]

    print(f'Possible historian trios: {part1(computer_links)}')
    print(f'LAN password: {part2(computer_links)}')
