#! /usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

day = '01'
test_assertion_a = 7
test_assertion_b = 5

def part_a(lines):
    depths = [int(line) for line in lines if line != '']
    count = 0
    for i in range(len(depths)-1):
        if depths[i] < depths[i+1]:
            count += 1
    return count

def part_b(lines):
    depths = [int(line) for line in lines if line != '']
    count = 0
    for i in range(len(depths)-3):
        if sum(depths[i:i+3]) < sum(depths[i+1:i+4]):
            count += 1
    return count

aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)

