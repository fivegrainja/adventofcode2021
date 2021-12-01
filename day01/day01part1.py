#! /usr/bin/env python3

import sys
import os
from rich import print

# Add parent directory to path to get aoc_utils
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import aoc_utils

day = '01'
test_assertion = 7

def count_depth_increases(lines):
    depths = [int(line) for line in lines if line != '']
    count = 0
    for i in range(len(depths)-1):
        if depths[i] < depths[i+1]:
            count += 1
    return count

aoc_utils.test_and_execute(count_depth_increases, day, test_assertion)

