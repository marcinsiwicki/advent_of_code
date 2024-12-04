"""
Advent of Code 2023: Day 2
"""
import re


N_RED = 12
N_GREEN = 13
N_BLUE = 14


def part1(gmap: dict) -> int:
    """Evaluate valid results."""
    # to determine if a given game is valid, need max of each color and compare to upper limit
    total = 0
    for id, res in gmap.items():
        max_red = max(d.get("red", 0) for d in res)
        max_green = max(d.get("green", 0) for d in res)
        max_blue = max(d.get("blue", 0) for d in res)

        if max_red <= N_RED and max_green <= N_GREEN and max_blue <= N_BLUE:
            total += id
    
    return total


def part2(gmap: dict) -> int:
    """Find lcd of colors and sum product over all games."""
    total = 0
    for id, res in gmap.items():
        max_red = max(d.get("red", 0) for d in res)
        max_green = max(d.get("green", 0) for d in res)
        max_blue = max(d.get("blue", 0) for d in res)

        total += max_red * max_green * max_blue

    return total


if __name__ == '__main__':
    with open('advent_of_code/2023/day02/input.txt', 'r') as f:
        raw_games = f.readlines()

    # game structure is id: subsets
    # subset structure is X red Y blue Z green
    # games_map {1: [{red: , green: , blue }, {red: , green: , blue: }]}

    games_map = {}
    for g in raw_games:
        gameid, results = g.split(':')
        id = int(gameid.split(' ')[-1])
        games_map[id] = []

        subsets = results.split(';')
        for subset in subsets:
            colors = re.findall(r"\d+\s+\w+", subset)
            subset_result = {i.split(" ")[-1]: int(i.split(" ")[0]) for i in colors}
            games_map[id].append(subset_result)

    print(part1(games_map))
    print(part2(games_map))
