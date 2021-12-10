#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

# import collections # https://docs.python.org/3/library/collections.html
# import numpy # https://numpy.org/doc/stable/user/quickstart.html
# import pandas # https://pandas.pydata.org/docs/getting_started/index.html#getting-started
# import itertools # https://docs.python.org/3/library/itertools.html
# import more_itertools # https://github.com/more-itertools/more-itertools
# import operator # https://docs.python.org/3/library/operator.html#module-operator

# import networkx # https://networkx.org/documentation/stable/tutorial.html
# import networkx as nx
# import matplotlib.pyplot as plt
# g1 = nx.petersen_graph()
# nx.draw(g1)
# plt.show()


day = '00'
test_assertion_a = None
test_assertion_b = None

def part_a(lines):
    # nums = [int(l) for l in lines if l != '']
    return

def part_b(lines):
    # nums = [int(l) for l in lines if l != '']
    return

# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
