"""
Advent of Code 2024: Day 12
"""


def check_adjacent(coords, eval_region):
    """Helper function to check if any adjacent coords in list."""
    # coords are adjacent if they share a row and are one apart on col
    # or share a col and are one apart on row
    for eval_coord in eval_region:
        delta = eval_coord - coords
        if abs(delta) == 1:
            return True
    return False


def get_regions(garden: list[list[str]]) -> dict:
    """
    Helper function to generate dict of regions with plant key

    Args:
        garden (list[list[str]]): raw input

    Returns:
        dict: regions by key 
    """
    # go through the whole garden, build a map of plant to locations
    # then go through each plant and find the adjacent regions
    plant_map = {}
    for i, row in enumerate(garden):
        for j, plant in enumerate(row):
            if plant in plant_map:
                plant_map[plant].append(complex(i, j))
            else:
                plant_map[plant] = [complex(i, j)]

    region_map = {}
    for plant, coors in plant_map.items():
        regions = []
        # loop through coords and find regions
        while coors:
            new_region = True
            curr = coors.pop(0)
            for region in regions:
                if check_adjacent(curr, region):
                    region.add(curr)
                    new_region = False
            if new_region:
                regions.append(set([curr]))
        # edge case can arise with leftmost being loose
        # maybe define it via set operations to re-unify
        for i in range(len(regions)):
            for j in range(len(regions)):
                if i == j:
                    continue
                lead_region, lag_region = regions[i], regions[j]
                if lead_region and lag_region and set(lead_region) & set(lag_region):
                    regions[i] = lead_region | lag_region
                    regions[j] = None
        # convert to list and order by row/col
        region_map[plant] = []
        for region in regions:
            if region:
                s_r = list(region)
                s_r.sort(key=lambda x: (x.real, x.imag))
                region_map[plant].append(s_r)

    return region_map


def part1(garden: list[list[str]]) -> int:
    """
    Given a garden, find the relevant plots and return sum of area * perim
    for all garden regions.

    A region is an unbroken string of the same char.

    Args:
        garden (list[list[str]]): grid of plants (represented by char)

    Returns:
        int: sum of all area * perims for each region
    """

    def calculate_perim(local_region):
        # project onto a grid and then iterate through it to see where the edges are
        x_offset= min(x.imag for x in local_region)
        x_max = max(x.imag for x in local_region)
        y_offset = min(x.real for x in local_region)
        y_max = max(x.real for x in local_region)
        grid_width = int(x_max - x_offset)+1
        grid_height = int(y_max - y_offset)+1

        # create empty grid [['', ''], ['', '']]
        grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        for c in local_region:
            y = int(c.real - y_offset)
            x = int(c.imag - x_offset)
            grid[y][x] = 1

        n_rows = len(grid)
        n_cols = len(grid[0])
        perim = 0
        for i in range(n_rows):
            for j in range(n_cols):
                if grid[i][j] == 1:
                    cell_perim = 4
                    if i > 0 and grid[i-1][j] == 1: # check left
                        cell_perim -= 1
                    if i < (n_rows - 1) and grid[i+1][j] == 1: # check right
                        cell_perim -= 1
                    if j > 0 and grid[i][j-1] == 1: # check above
                        cell_perim -= 1
                    if j < (n_cols - 1) and grid[i][j+1] == 1: # check below
                        cell_perim -= 1
                    perim += cell_perim

        return perim

    region_map = get_regions(garden)

    # calculate perims and areas
    # add up all the side lengths along a row/col in the region
    measurements = []
    for plant, regions in region_map.items():
        for region in regions:
            area = len(region)
            perim = calculate_perim(region)
            #print(f'Region {plant} has area {area} and perimeter {perim}')
            measurements.append((area, perim))

    return sum(a * p for a, p in measurements)


def part2(garden: list[list[str]]) -> int:
    """Return number of sides instead of perim."""

    def calculate_sides(local_region):
        # project onto a grid and then iterate through it to see where the edges are
        x_offset= min(x.imag for x in local_region)
        x_max = max(x.imag for x in local_region)
        y_offset = min(x.real for x in local_region)
        y_max = max(x.real for x in local_region)
        grid_width = int(x_max - x_offset)+1
        grid_height = int(y_max - y_offset)+1

        # create empty grid [['', ''], ['', '']]
        grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        for c in local_region:
            y = int(c.real - y_offset)
            x = int(c.imag - x_offset)
            grid[y][x] = 1

        n_rows = len(grid)
        n_cols = len(grid[0])
        corners = 0 # the number of corners == number of sides
        # corners exist when three of the cells surrounding the corner are the same
        for i in range(n_rows):
            for j in range(n_cols):
                if grid[i][j] == 1:
                    if i == 0:
                        for cond in ((j == 0), (j == (n_cols-1)), (j > 0 and grid[i][j-1] == 0),
                                     (j < (n_cols-1) and grid[i][j+1] == 0)):
                            if cond:
                                corners += 1
                    if i == n_rows-1:
                        for cond in ((j == 0), (j == (n_cols-1)),(j > 0 and grid[i][j-1] == 0),
                                     (j < (n_cols-1) and grid[i][j+1] == 0)):
                            if cond:
                                corners += 1
                    if j == 0:
                        for cond in ((i > 0 and grid[i-1][j] == 0), (i < (n_rows-1) and grid[i+1][j] == 0)):
                            if cond:
                                corners += 1
                    if j == (n_cols-1):
                        for cond in  ((i > 0 and grid[i-1][j] == 0), (i < (n_rows-1) and grid[i+1][j] == 0)):
                            if cond:
                                corners += 1
                    if i > 0:
                        if j > 0:
                            if ((grid[i][j-1] == grid[i-1][j] == 1 and grid[i-1][j-1] == 0) # bottom right outside
                                | (grid[i][j-1] == grid[i-1][j-1] == grid[i-1][j] == 0)): # upper left inside
                                corners += 1
                        if j < n_cols-1:
                            if ((grid[i-1][j] == grid[i][j+1] == 1 and grid[i-1][j+1] == 0) # bottom left outside
                                | (grid[i-1][j] == grid[i-1][j+1] == grid[i][j+1] == 0)): # upper right inside
                                corners += 1
                            if grid[i-1][j+1] == 1 and grid[i-1][j] == grid[i][j+1] == 0: # kissing diag
                                corners += 2
                    if i < n_rows-1:
                        if j > 0:
                            if ((grid[i][j-1] == grid[i+1][j-1] == grid[i+1][j] == 0) # bottom left inside
                                | (grid[i][j-1] == grid[i+1][j] == 1 and grid[i+1][j-1] == 0)): # upper right outside
                                corners += 1
                        if j < n_cols-1:
                            if ((grid[i][j+1] == grid[i+1][j] == grid[i+1][j+1] == 0) # bottom right outside
                                | (grid[i+1][j] == grid[i][j+1] == 1 and grid[i+1][j+1] == 0)): # upper left outside
                                corners += 1
                            if grid[i+1][j+1] == 1 and grid[i][j+1] == grid[i+1][j] == 0: # kissing diag
                                corners += 2

        return corners

    region_map = get_regions(garden)

    # calculate perims and areas
    # add up all the side lengths along a row/col in the region
    measurements = []
    for plant, regions in region_map.items():
        for region in regions:
            area = len(region)
            sides = calculate_sides(region)
            # print(f'Region {plant} has area {area} and sides {sides}')
            measurements.append((area, sides))

    return sum(a * s for a, s in measurements)


if __name__ == '__main__':
    with open('advent_of_code/2024/day12/input.txt', 'r') as f:
        input_garden = f.readlines()
    input_garden = [list(l.strip()) for l in input_garden]

    print(f'Cost of fence (perim): {part1(input_garden)}')
    print(f'Cost of fence (sides): {part2(input_garden)}')
