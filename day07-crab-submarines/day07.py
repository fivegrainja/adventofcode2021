#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import collections

day = '07'
test_assertion_a = 37
test_assertion_b = 168


def part_a(lines):
    crab_positions = sorted([int(p) for p in lines[0].split(',')])
    max_position = crab_positions[-1]
    # crabs_at_positions represents how many crabs are at each position
    crabs_at_positions = [0] * (max_position + 1)
    for crab in crab_positions:
        crabs_at_positions[crab] += 1
    # Strategy - The cost for moving all crabs to position P is the sum of
    # 1. The cost of moving all crabs to the left of P to P and
    # 2. The cost of moving all the crabs to the right of P to P
    # Working from left to right we calculate the cost of moving all the crabs to the left
    # of each position to that position (cost_left). This is O(N) time.
    # Then we do the mirror - work from right to left calculating the cost of moving all the
    # crabs to the right of each position to that position (cost_right). Also O(N) time.
    # Then at each position sum the values of cost_left and cost_right to get the total
    # cost of moving all crabs to that position.
    cost_left = [0] * (max_position + 1)
    num_crabs_left = 0
    for pos in range(len(cost_left)):
        if pos > 0:
            # Start with the cost of the previous position
            cost_left[pos] += cost_left[pos-1]
            # Add the crabs at position-1 to the total number to the left
            num_crabs_left += crabs_at_positions[pos-1]
            # Add the cost of moving all the crabs to the left one more position
            cost_left[pos] += num_crabs_left
    # Repeat as above, except from the right
    cost_right = [0] * (max_position + 1)
    num_crabs_right = 0
    for pos in range(len(cost_right) - 1, -1, -1):
        if pos < len(cost_right) - 1:
            cost_right[pos] += cost_right[pos + 1]
            num_crabs_right += crabs_at_positions[pos+1]
            cost_right[pos] += num_crabs_right
    cost = [cost_left[i] + cost_right[i] for i in range(max_position + 1)]
    return min(cost)


def part_b(lines):
    crab_positions = sorted([int(p) for p in lines[0].split(',')])
    max_position = crab_positions[-1]
    crabs_positions = collections.Counter(crab_positions)
    cost = [0] * (max_position + 1)
    # Brute force seems sloppy, but can't think of a better way at the moment.
    for pos, count in crabs_positions.items():
        step_cost = 0
        for p in range(pos - 1, -1, -1):
            step_cost += count * abs(p - pos)
            cost[p] += step_cost
        step_cost = 0
        for p in range(pos + 1, max_position + 1):
            step_cost += count * abs(p - pos)
            cost[p] += step_cost
    return min(cost)


aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
