#! /usr/bin/env python3

import sys
from rich import print
from pprint import pprint
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import math

day = '09'
test_assertion_a = 15
test_assertion_b = 1134

def get_neighbors(map, row_i, col_i):
    """ return list of (row_i)(col_i)
    """
    neighbors = []
    if row_i > 0:
        neighbors.append((row_i - 1, col_i))
    if row_i < len(map) - 1:
        neighbors.append((row_i+1, col_i))
    if col_i > 0:
        neighbors.append((row_i, col_i - 1))
    if col_i < len(map[0]) - 1:
        neighbors.append((row_i, col_i + 1))
    return neighbors


def get_local_mins(map):
    """ returns list of (row_i, col_i)
    """
    local_mins = []
    for row_i in range(len(map)):
        for col_i in range(len(map[row_i])):
            neighbors = get_neighbors(map, row_i, col_i)
            neighbor_heights = [map[nr_i][nc_i] for nr_i, nc_i in neighbors]
            if map[row_i][col_i] < min(neighbor_heights):
                local_mins.append((row_i,col_i))
    return local_mins


def part_a(lines):
    """ Return the sum of all the local minimum in the map
    """
    map = [[int(h) for h in line] for line in lines]
    local_mins = get_local_mins(map)
    return sum([map[row_i][col_i] + 1 for (row_i, col_i) in local_mins])


def part_b(lines):
    """ Return the product of the sizes of the three largest basins in the map.
    A basin
    """
    map = [[int(h) for h in line] for line in lines]
    local_mins = get_local_mins(map)
    basin_sizes = []
    for local_min in local_mins:
        to_visit = set([local_min])
        visited = set()
        while to_visit:
            row_i, col_i = to_visit.pop()
            visited.add((row_i, col_i))
            for neighbor in get_neighbors(map, row_i, col_i):
                if neighbor not in visited and neighbor not in to_visit:
                    if map[neighbor[0]][neighbor[1]] != 9:
                        to_visit.add(neighbor)
        basin_sizes.append(len(visited))
    basin_sizes.sort()
    return math.prod(basin_sizes[-3:])


aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
