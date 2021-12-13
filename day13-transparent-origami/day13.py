#! /usr/bin/env python3

# See day<number>-questions.txt for context to this solution

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

day = '13'
test_assertion_a = 17
test_assertion_b = None


def get_dots_and_folds(lines):
    """ Return (dots, folds) from the input lines where
    dots is a set of (x,y) coordinates
    folds is a list of '<axis>=<fold index>' instructions
    """
    line_iter = iter(lines)
    dots = set()
    while line := next(line_iter):
        x, y = line.split(',')
        dots.add((int(x), int(y)))
    folds = []
    for line in line_iter:
        folds.append(line.split()[-1])
    return (dots, folds)


def do_fold(dots, fold):
    """ Perform the operation as indicated by fold and described in the question. Returns None
    but modifies dots in place to reflect the fold.

    Strategy: Iterate through the dots. For any that need to be moved as a result of the fold do two steps:
    1. Calculate the post-fold coordinates for this dot and add to the dots_to_add set.
    2. Add the pre-fold dot to the dots_to_remove set
    Once we have processed every dot that needs to be folded take two more steps:
    3. Remove from dots all the dots in dots_to_remove (these were the dots on the side that got folded)
    4. Add to dots all the dots in dots_to_add (these are the new coordinates of the dots that were folded)
    """
    axis, pivot = fold.split('=')
    pivot = int(pivot)
    dots_to_remove = set()
    dots_to_add = set()
    for dot in dots:
        if axis == 'x' and dot[0] > pivot:
            dots_to_remove.add(dot)
            dots_to_add.add((pivot - (dot[0] - pivot), dot[1]))
        elif axis == 'y' and dot[1] > pivot:
            dots_to_remove.add(dot)
            dots_to_add.add((dot[0], pivot - (dot[1] - pivot)))
    dots -= dots_to_remove
    dots |= dots_to_add


def part_a(lines):
    """ Return the number of dots after the first fold instruction
    """
    dots, folds = get_dots_and_folds(lines)
    do_fold(dots, folds[0])
    return len(dots)


def part_b(lines):
    """ Perform all fold instructions and print out the resulting grid. The interpretation of the capital
    letters represented by the dots in the grid is a manual step.
    """
    dots, folds = get_dots_and_folds(lines)
    for fold in folds:
        do_fold(dots, fold)
    max_x = max([dot[0] for dot in dots])
    max_y = max([dot[1] for dot in dots])
    grid = [[' ' for x in range(max_x + 1)] for y in range(max_y + 1)]
    for dot in dots:
        grid[dot[1]][dot[0]] = '*'
    for row in grid:
        print(''.join(row))


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
