#! /usr/bin/env python3

# See day14-questions.txt for context to this solution

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

import collections # https://docs.python.org/3/library/collections.html
import itertools # https://docs.python.org/3/library/itertools.html

day = '14'
test_assertion_a = 1588
test_assertion_b = 2188189693529


# Read lines from the input file
def read_polymer_and_replacements(lines):
    """ Parse input lines and return initial polymer and the replacement mappings
    """
    polymer = list(lines[0])
    replacements = {}
    for line in lines[2:]:
        pair, _, to_insert = line.split()
        replacements[pair] = to_insert
    return polymer, replacements


def do_insertion(polymer, replacements):
    """ For part a, take a given polymer and perform one iteration of the growth
    process, returning the resulting polymer.
    Note: this works, but turns out to be unworkably slow for part b.
    """
    new_polymer = []
    for left, right in itertools.pairwise(polymer):
        new_polymer.extend([left, replacements[left + right]])
    new_polymer.append(polymer[-1])
    return new_polymer


def part_a(lines):
    """ Perform the given grown strategy for 10 iterations. Return the difference
    between the final counts of the most frequent and least frequent elements
    in the final polymer.

    Note: This approach doesn't work for part b. The solution to part b would work for
    this part, but I've left my original solution to part a to demonstrate my initial
    approach to this problem.
    """
    polymer, replacements = read_polymer_and_replacements(lines)
    for i in range(10):
        polymer = do_insertion(polymer, replacements)
    counts_sorted = collections.Counter(polymer).most_common()
    # The above most_common() call returns a liste of (polymer, count) sorted by count descending
    # Subtract the last count from the first count to get the return value
    return counts_sorted[0][1] - counts_sorted[-1][1]


def get_counts_from_pairs(pairs, polymer):
    """ Given a dictionary of counts of pairings of elements return the 
    count of each element. Each element will appear in two pairings (once on the left
    and once on the right) except for the first and last elements of the polymer.
    """
    counts = collections.defaultdict(lambda: 0)
    # Just count the left element of each pair. This gets rid of the duplicates, includes the first
    # element in polymer, but will not count the very last element
    for (left, right), count in pairs.items():
        counts[left] += count
    # Count that very last element
    counts[polymer[-1]] += 1
    return counts


def part_b(lines):
    """ Starting with the given polymer apply the growth mapping 40 times and return
    the different between the counts of the most common and least common elements in
    the final polymer.

    Strategy
    The approach used it part A won't work, it doesn't scale to this degree.
    Instead of actually building the polymer for each iteration of growth, instead just
    track pairs of adjacent elements and how many times each pair appears. Each iteration
    take each pair, calculate the 2 new pairs created from it, and remember that you create
    as many of those new pairs as you had of the original pair.

    Example:
    polymer = 'abab'
    adjacent_pairs = 'ab' twice and 'ba once'
    insertion rules  'ab'->x and 'ba'->y
    'ab' twice results in 'ax' twice and 'xb' twice
    'ba' once results in 'by' once and 'ya' once
    Throw out the previous adjacent_pairs and build a new one using the results from this iteration.
    So after one iteration you have adjacent_pairs = 'ax' twice, 'bx' twice, 'by' once, 'y' once
    Then repeat N times.

    Counting results at the end is a bit tricky. Every element in the polymer will appear twice, once as
    the left element of a pair and once as the right element of a pair. Except for the very first and last
    elements in the polymer, which will only appear in a single pair. The adjacent_pairs structure
    doesn't maintain order, so we can't use it to determine the first and last element. But we can refer
    back to the original polymer to do that.
    """
    polymer, replacements = read_polymer_and_replacements(lines)
    # pairs is a dictionary where the keys are strings of len 2 representing an adjancent pair
    # of elements. The values are the number of times that pair occurs in the polymer.
    pairs = collections.Counter([l + r for (l, r) in itertools.pairwise(polymer)])
    for i in range(40):
        new_pairs = collections.defaultdict(lambda: 0) # Dictionary with a default of 0 for unknown keys
        for (left, right), count in pairs.items():
            new_pairs[left + replacements[left + right]] += count
            new_pairs[replacements[left + right] + right] += count
        pairs = new_pairs

    counts = get_counts_from_pairs(pairs, polymer)
    return max(counts.values()) - min(counts.values())


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
