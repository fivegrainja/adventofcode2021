#! /usr/bin/env python3

# See day15-questions.txt for context to this solution

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

import heapq # https://docs.python.org/3/library/heapq.html
import networkx  as nx # https://networkx.org/documentation/stable/tutorial.html

day = '15'
test_assertion_a = 40
test_assertion_b = 315


def get_neighbors(position, grid_dimension):
    """ Given a position (row index, col index) and the length of a side of the grid, return
    a list of tuples representing the grid coordinates for the horizonal and vertical neighbors
    """
    neighbors = []
    if position[0] > 0:
        neighbors.append((position[0] - 1, position[1]))
    if position[0] < grid_dimension - 1:
        neighbors.append((position[0] + 1, position[1]))
    if position[1] > 0:
        neighbors.append((position[0], position[1] - 1))
    if position[1] < grid_dimension - 1:
        neighbors.append((position[0], position[1] + 1))
    return neighbors


def heuristic(a, b):
    """ Return the Manhattan distance, a measure of the distance from one cell of a grid to another cell
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, dest, heuristic):
    """ Search the grid finding the least expensive path from start to dest. Return the cost of that
    least expensive path.
    For a great introduction to A* see https://www.redblobgames.com/pathfinding/a-star/introduction.html
    """
    frontier = [(0, start)]
    came_from = dict()
    cost = dict()
    came_from[start] = None
    cost[start] = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == dest:
            break
        for next in get_neighbors(current, len(grid)):
            new_cost = cost[current] + grid[next[0]][next[1]]
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost + heuristic(dest, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    return cost[dest]


def part_a(lines):
    """ Return the cost of the least expensive path from upper left to lower right of grid
    """
    grid = [[int(c) for c in line] for line in lines]
    dest_cost = a_star(grid, (0,0), (len(grid) - 1, len(grid) - 1), heuristic)
    return dest_cost


def expand_grid(grid, n):
    """ Expand the grid 5x in each direction, increasing cost according to question description.
    """
    dim = len(grid)
    # copy horizontally
    for copy_i in range(1, 5):
        for row_i in range(dim):
            for col_i in range(copy_i * dim, copy_i * dim + dim):
                base_value = grid[row_i][col_i - dim]
                # Cost above 9 wraps back to 1
                grid[row_i].append(base_value + 1 if base_value < 9 else 1)
    # copy vertically
    for copy_i in range(1, 5):
        for row_i in range(copy_i * dim, copy_i * dim + dim):
            grid.append([])
            for col_i in range(len(grid[0])):
                base_value = grid[row_i - dim][col_i]
                # Cost above 9 wraps back to 1
                grid[row_i].append(base_value + 1 if base_value < 9 else 1)


def part_b(lines):
    """ Return the cost of the least expensive path from upper lift to lower right
    but on the expanded grid instead of the original input.
    """
    grid = [[int(c) for c in line] for line in lines]
    expand_grid(grid, 5)
    dest_cost = a_star(grid, (0,0), (len(grid) - 1, len(grid) - 1), heuristic)
    return dest_cost

# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
