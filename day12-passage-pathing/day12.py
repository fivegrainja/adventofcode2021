#! /usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import string
import collections # https://docs.python.org/3/library/collections.html

day = '12'

# The question gives several test inputs. These values are for the first, smallest test input.
test_assertion_a = 10
test_assertion_b = 36

# We represent the graph as an adjancency map. For each node in the graph, this dict stores the set
# of nodes that are adjacent to that node.
def build_adjacency_map(lines):
    adj_map = {}
    for line in lines:
        a, b = line.split('-')
        if a not in adj_map:
            adj_map[a] = set()
        adj_map[a].add(b)
        if b not in adj_map:
            adj_map[b] = set()
        adj_map[b].add(a)
    return adj_map


# build_paths is called recursively to build all the possible paths according to the rules of the question.
# Strategy:
# - Given a partial path into the graph, create a list of all paths from that point to 'end'
# - Start by considering each neighbor of the last node in the path (i.e. all the nodes we could go to next)
# -   If that neighbor is 'end' then we've found a path to the end, add it to our list
# -   Otherwise if it would be valid to add that neighbor to path then call build_paths recursively
#      passing path + [neighbor] as the new path.
# -   Add any results from this build_paths call to our results
# - Return the list of all the paths we found
#
# Note that for part b the rules allow us to visit a single small cave twice. So for part b we start by calling
# build_paths with allow_dupe_small=True. Any time we visit a small cave a 2nd time then further recursive calls
# after that point pass allow_dupe_small=False so another small cave isn't visited twice on that path.
def build_paths(map, path_so_far, allow_dupe_small):
    """ Return a list of possible continuations of path_so_far.
    Return list of lists.
    """
    # possible_next_steps is always the neighbors of the last node in path_so_far
    possible_next_steps = map[path_so_far[-1]]
    # results will be all the valid paths starting with path_so_far to 'end'
    results = []
    for step in possible_next_steps:
        if step == 'end':
            # One of the neighbors was 'end' so add this to the list of results
            results.append(path_so_far + ['end'])
        elif step == 'start':
            # Don't traverse start again, for either part a or b
            pass
        elif step[0] in string.ascii_uppercase:
            # Big caves (uppercase) can always be visited more than once
            results.extend(build_paths(map, path_so_far + [step], allow_dupe_small))
        elif step[0] in string.ascii_lowercase:
            if step in path_so_far:
                # This neighbor cave is lowercase and we've visited it before in this path
                if allow_dupe_small:
                    # We can allow a 2nd visit to a small cave on this path
                    # Passing allow_dupe_small=False to prevent another small cave from being added
                    # to this path a 2nd time.
                    results.extend(build_paths(map, path_so_far + [step], False))
                else:
                    # This neighbor is in path and allow_dupe_small is False
                    pass
            else:
                # Neighbor is a small cave and does not appear in path already, so add.
                results.extend(build_paths(map, path_so_far + [step], allow_dupe_small))
    return results


def part_a(lines, allow_dupe_small=False):
    """ Return the number of paths from 'start' to 'end'.
    allow_dupe_small is False for part a
    """
    map = build_adjacency_map(lines)
    paths = build_paths(map, ['start'], allow_dupe_small)
    return len(paths)


def part_b(lines):
    """ Return the number of paths from 'start' to 'end'
    allow_dupe_small is True, telling build_paths that a single small cave can be visited twice
    in any given path.
    """
    return part_a(lines, True)


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
