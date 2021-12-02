#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

# import collections # https://docs.python.org/3/library/collections.html
# import networkx # https://networkx.org/documentation/stable/tutorial.html
# import numpy # https://numpy.org/doc/stable/user/quickstart.html
# import pandas # https://pandas.pydata.org/docs/getting_started/index.html#getting-started
# import itertools # https://docs.python.org/3/library/itertools.html
# import more_itertools # https://github.com/more-itertools/more-itertools
# import operator # https://docs.python.org/3/library/operator.html#module-operator

day = '00'
test_assertion_a = None
test_assertion_b = None

def part_a(lines):
    # nums = [int(l) for l in lines if l != '']
    return

def part_b(lines):
    # nums = [int(l) for l in lines if l != '']
    return

aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
