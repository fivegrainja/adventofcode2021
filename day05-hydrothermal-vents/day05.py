#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import parse
import itertools

day = '05'
test_assertion_a = 5
test_assertion_b = 12

def read_input(raw_input):
    """ Return max value of x, max value of y, and a list of [x1, y1, x2, y2] lists representing
    the lines in the input.
    Note that elements of raw_input are the raw format from the input files of this format:
    x1,y1 -> x2,y2
    """
    lines = []
    max_x = 0
    max_y = 0
    for l in raw_input:
        r = parse.parse('{x1:d},{y1:d} -> {x2:d},{y2:d}', l)
        lines.append((r['x1'], r['y1'], r['x2'], r['y2']))
        max_x = max(max_x, r['x1'], r['x2'])
        max_y = max(max_y, r['y1'], r['y2'])
    return (max_x, max_y, lines)

def populate_field(lines, field, ignore_diags=True):
    """ Take each of the lines and increment by one each point in field that each line
    touches. If ignore_diags then ignore diagonal lines.
    """
    for line in lines:
        x1, y1, x2, y2 = line
        # Only consider horizonal or vertical lines
        if x1 != x2 and y1 != y2:
            if not ignore_diags:
                if x1 < x2:
                    x_iter = range(x1, x2 + 1)
                else:
                    x_iter = range(x1, x2 - 1, -1)
                if y1 < y2:
                    y_iter = range(y1, y2 + 1)
                else:
                    y_iter = range(y1, y2 - 1, -1)
                for x, y in zip(x_iter, y_iter):
                    field[y][x] += 1
        elif y1 == y2:
            # horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                field[y1][x] += 1
        elif x1 == x2:
            # vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                field[y][x1] += 1
        else:
            raise Exception('Inconceivable!')


def count_overlaps(field):
    """ Count the points in field with a value greater than 1 (indicating that more than
    one line intersected that point.)
    """
    all_points = itertools.chain(*field)
    num_overlaps = len([i for i in all_points if i > 1])
    return num_overlaps


def part_a(raw_input, ignore_diags=True):
    max_x, max_y, lines = read_input(raw_input)
    # Note that our field dimentions need to be one greater than max_x and max_y to
    # account for 0-indexing of the ranges.
    field = [[0 for i in range(max_x + 1)] for j in range(max_y + 1)]
    # Increment values in field where lines exist
    populate_field(lines, field, ignore_diags=ignore_diags)
    # Return number of values in fields that are greater than 1
    return count_overlaps(field)


def part_b(lines):
    # Same as part_a, except include diagonal lines.
    return part_a(lines, ignore_diags=False)

aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
