#! /usr/bin/env python3

# See day17-questions.txt for context to this solution

from functools import cache
import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import parse


day = '17'
test_assertion_a = 45
test_assertion_b = 112


def does_hit_target(initial_x_speed, initial_y_speed, target_x_left, target_x_right, target_y_top, target_y_bottom):
    y = x = 0
    speed_x = initial_x_speed
    speed_y = initial_y_speed
    max_y = 0
    # print(f'{initial_y_speed=}')
    while y >= target_y_bottom and x <= target_x_right:
        # print(f'  {y=} {speed_y=}')
        max_y = max(max_y, y)
        if y <= target_y_top and x >= target_x_left:
            # We hit it
            return (True, max_y)
        y += speed_y
        x += speed_x
        speed_y -= 1
        speed_x = speed_x - 1 if speed_x > 0 else 0
    return (False, None)


@cache
def find_ways_to_hit_target(target_x_left, target_x_right, target_y_top, target_y_bottom):
    count = 0
    max_y = 0
    # Observation: For any positive initial y speed, the probe will end up at y=0 with speed of negative its initial speed.
    # So we need to test all possible y initial speeds between +/- target_y_bottom
    # Observation: The maximum initial x speed would be the difference between the origin and the right side of the target area.
    # So we need to test all possible x initial speeds between 0 and target_x_right
    for speed_y in range(abs(target_y_bottom), target_y_bottom-1, -1):
        for speed_x in range(target_x_right + 1):
            (hit_target, this_max_y) = does_hit_target(speed_x, speed_y, target_x_left, target_x_right, target_y_top, target_y_bottom)
            if hit_target:
                count += 1
                max_y = max(max_y, this_max_y)
    return (count, max_y)


# We really only need one of these functions below. But due to the way I've setup test_and_execute it's easier
# to just have a separate part_a and part_b. This is the reason for the @cache on find_ways_to_hit_target, it
# gets called for each part with the exact same arguments, so doesn't need to calculate more than once.

def part_a(lines):
    r = parse.parse('target area: x={:n}..{:n}, y={:n}..{:n}', lines[0])
    target_x_left, target_x_right, target_y_bottom, target_y_top = r.fixed
    count, max_y = find_ways_to_hit_target(target_x_left, target_x_right, target_y_top, target_y_bottom)
    return max_y


def part_b(lines):
    r = parse.parse('target area: x={:n}..{:n}, y={:n}..{:n}', lines[0])
    target_x_left, target_x_right, target_y_bottom, target_y_top = r.fixed
    count, max_y = find_ways_to_hit_target(target_x_left, target_x_right, target_y_top, target_y_bottom)
    return count

# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
