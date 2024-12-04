"""
Advent of Code 2024: Day 4
"""


def find_xmas(input_matrix, row, col):
    """Find instances of XMAS string"""

    # given a start character, search in each direction for remaining characters
    # make eight new strings and check them for XMAS
    # can search only in the directions open confined to grid

    n_rows = len(input_matrix)
    n_cols = len(input_matrix[0])

    possible_lines = []
    iteration_amounts = [
        (0, 1), (0, -1), (-1, 0), (1, 0),
        (1, 1), (-1, -1), (-1, 1), (1, -1)]

    for direction in iteration_amounts:
        # if string would exceed the grid, skip it
        max_row = row + 3 * direction[0]
        max_col = col + 3 * direction[1]
        if max_row < 0 or max_row > (n_rows - 1):
            continue
        if max_col < 0 or max_col > (n_cols - 1):
            continue

        s = ''
        for i in range(4):
            r = row + i * direction[0]
            c = col + i * direction[1]
            s += input_matrix[r][c]
        possible_lines.append(s)

    matches = sum([1 for s in possible_lines if s == 'XMAS'])

    return matches


def find_mas(input_matrix, row, col):
    """Find MAS string in an X shape."""
    n_rows = len(input_matrix)
    n_cols = len(input_matrix[0])

    matches = 0
    match_strings = ['MAS', 'SAM']

    # only one orientation that results in valid string: x
    if col > 0 and col < (n_cols-1) and row > 0 and row < (n_rows-1):
        s_1 = input_matrix[row-1][col-1] + 'A' + input_matrix[row+1][col+1]
        s_2 = input_matrix[row-1][col+1] + 'A' + input_matrix[row+1][col-1]
        if s_1 in match_strings and s_2 in match_strings:
            matches += 1

    return matches


def part1(word_puzzle: list) -> int:
    """Search for all XMAS words within puzzle."""
    # find the anchor X character
    # search around it in each direction finding the rest of the chars 
    # create a matrix of the word puzzle
    word_matrix = [list(l.strip()) for l in word_puzzle]

    total = 0

    n_rows = len(word_matrix)
    n_cols = len(word_matrix[0])

    for i in range(n_rows):
        for j in range(n_cols):
            if word_matrix[i][j] == 'X':
                total += find_xmas(word_matrix, i, j)

    return total


def part2(word_puzzle: list) -> int:
    """Find MAS X."""
    word_matrix = [list(l.strip()) for l in word_puzzle]
    total = 0

    n_rows = len(word_matrix)
    n_cols = len(word_matrix[0])

    for i in range(n_rows):
        for j in range(n_cols):
            if word_matrix[i][j] == 'A':
                total += find_mas(word_matrix, i, j)
    
    return total

if __name__ == '__main__':
    with open('advent_of_code/2024/day04/input.txt', 'r') as f:
        puzzle = f.readlines()

    print(f"XMAS count: {part1(puzzle)}")
    print(f"MAS in X count: {part2(puzzle)}")
