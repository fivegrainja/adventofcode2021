#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

import collections # https://docs.python.org/3/library/collections.html
# import networkx # https://networkx.org/documentation/stable/tutorial.html
# import numpy # https://numpy.org/doc/stable/user/quickstart.html
# import pandas # https://pandas.pydata.org/docs/getting_started/index.html#getting-started
# import itertools # https://docs.python.org/3/library/itertools.html
# import more_itertools # https://github.com/more-itertools/more-itertools
# import operator # https://docs.python.org/3/library/operator.html#module-operator

day = '06'
test_assertion_a = 5934
test_assertion_b = 26984457539

MAX_AGE = 8
NUM_AGES = MAX_AGE + 1 # 0 is a valid age
SENIOR_DISCOUT = 2 # After generating a new fish at age 0 a fish becomes MAX_AGE - SENIOR_DISCOUNT


def build_first_generation(initial_population):
    first_gen = collections.Counter(initial_population)
    first_gen = [first_gen.get(age, 0) for age in range(NUM_AGES)]
    return [first_gen]


def build_next_generation(gens):
    next_gen = [0] * NUM_AGES
    # All fish at age zero generate a fish at age MAX_AGE 
    # They also themselves go to age SENIOR_DISCOUNT from end
    last_gen = gens[-1]
    next_gen[MAX_AGE] = last_gen[0]
    next_gen[MAX_AGE - SENIOR_DISCOUT] = last_gen[0]
    # Decrement all other ages, remembering to add so we don't overwrite the above
    for age in range(len(next_gen) - 1):
        next_gen[age] += last_gen[age+1]
    gens.append(next_gen)


def part_a(lines, num_days=80):
    initial_population = [int(p) for p in lines[0].split(',')]
    gens = build_first_generation(initial_population)
    for day in range(1, num_days|+1):
        build_next_generation(gens)
    return sum(gens[-1])


def part_b(lines):
    return part_a(lines, num_days=256)


aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
