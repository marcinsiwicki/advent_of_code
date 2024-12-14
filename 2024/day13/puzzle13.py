"""
Advent of Code 2024: Day 13
"""
import time
import numpy as np


def part1(in_games) -> int:
    """
    Solve the system of equations for each game. Has the form prize = xA + yB.
    """
    token_cost = 0
    for game in in_games:
        c1, c2 = game['prize']
        a1, a2 = game['A']
        b1, b2 = game['B']

        A = ((c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2))
        B = ((a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2))

        if A.is_integer() and B.is_integer():
            token_cost += (A * 3 + B * 1)

    return int(token_cost)


def part1_matrix(in_games) -> int:
    """Just for fun, do it with the matrices."""
    token_cost = 0
    for game in in_games:
        matA = np.matrix(list(zip(*[game['A'], game['B']])))
        matB = np.matrix(list(zip(game['prize'])))

        X = matA.I * matB
        A, B = X[0].item(0), X[1].item(0)
        if A.is_integer() and B.is_integer():
            token_cost += int(A * 3 + B * 1)

    return token_cost


def part2(in_games) -> int:
    """Solve with higher base vals"""
    token_cost = 0
    for game in in_games:
        c1, c2 = game['prize']
        c1 += 10000000000000
        c2 += 10000000000000
        a1, a2 = game['A']
        b1, b2 = game['B']

        A = ((c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2))
        B = ((a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2))

        if A.is_integer() and B.is_integer():
            token_cost += (A * 3 + B * 1)

    return int(token_cost)


if __name__ == '__main__':
    with open('advent_of_code/2024/day13/test.txt', 'r') as f:
        raw_games = f.readlines()

    # transform each game into a system of equations 
    games = []
    game = {}
    for l in raw_games:
        if ':' in l:
            params, res = l.split(':')
            if 'Button' in params:
                button = params.split('Button ')[1][0]
                x = res.split('X+')[1].split(',')[0]
                y = res.split('Y+')[1].strip()
                game[button] = (int(x), int(y))
            elif 'Prize' in params:
                x = res.split('X=')[1].split(',')[0]
                y = res.split('Y=')[1].strip()
                game['prize'] = (int(x), int(y))
                games.append(game)
                game = {}

    s = time.time()
    print(f'Tokens needed: {part1(games)} in {time.time() - s}')

    s = time.time()
    print(f'Tokens needed (matrix): {part1_matrix(games)} in {time.time() - s}')

    s = time.time()
    print(f'Tokens needed for larger machine: {part2(games)} in {time.time() - s}')
