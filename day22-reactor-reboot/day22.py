#! /usr/bin/env python3

# See day<number>-questions.txt for context to this solution

# from dataclasses import dataclass
import collections
import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import parse
import functools


day = '22'
test_assertion_a = 590784
test_assertion_b = 2758514936282235


class Cuboid:

    def __init__(self, state, x_min, x_max, y_min, y_max, z_min, z_max):
        self.state = state
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def is_within_50(self):
        """ Return true if cuboid is within 50 of the origin, False otherwise.
        The question states that all of the cuboid will be within that distance
        or none of it will, so we can get away by just testing one bound on
        each axis.
        """
        return -50 <= self.x_min <= 50 and -50 <= self.y_min <= 50 and -50 <= self.z_min <= 50
    
    def get_intersection(self, earlier):
        """ Return a cuboid that compensates for the imposing of self over earlier.
        """
        # Note that order matters.
        int_x_min = max(self.x_min, earlier.x_min)
        int_x_max = min(self.x_max, earlier.x_max)
        int_y_min = max(self.y_min, earlier.y_min)
        int_y_max = min(self.y_max, earlier.y_max)
        int_z_min = max(self.z_min, earlier.z_min)
        int_z_max = min(self.z_max, earlier.z_max)
        if int_x_min > int_x_max or int_y_min > int_y_max or int_z_min > int_z_max:
            return None
        # self is on, earlier is on -> intersection off
        # self is on, earlier is off -> intersection on
        # self is off, earlier is on -> intersection off
        # self is off, earlier is off -> intersection on
        state = (not self.state) if self.state == earlier.state else self.state
        return Cuboid(state, int_x_min, int_x_max, int_y_min, int_y_max, int_z_min, int_z_max)

    def volume(self):
        """ Return volume of this cuboid, negative if state is False
        """
        v = (self.x_max-self.x_min+1) * (self.y_max-self.y_min+1) * (self.z_max-self.z_min+1)
        if not self.state:
            v *= -1
        return v
    
    def __repr__(self):
        return f'({self.state},{self.x_min},{self.x_max},{self.y_min},{self.y_max},{self.z_min},{self.z_max})'


def part_a(lines, just_50=True):
    # Create cuboids for each line of input, throwing some out if just_50
    cuboids = []
    for line in lines:
        r = parse.parse('{:l} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}', line)
        cuboid = Cuboid(True if r.fixed[0] == 'on' else False, *r.fixed[1:])
        if (not just_50) or cuboid.is_within_50():
            cuboids.append(cuboid)
    # Iterate through cuboids in order, comparing to each already processed cuboid. Any time
    # we find an intersection with a previous cuboid create a new cuboid that corrects for that
    # intersection.
    #
    # This is horribly inefficient - worse than O(n^2) due to the added cuboids. A better solution would
    # be to decompose cuboids into smaller cuboids whenever subtracting from it. But the logic of creating
    # those subcuboids is more than I want to deal with at the moment.
    processed = [] # Original cuboids that we processed plus any intersection cuboids we create
    for this_cuboid in cuboids:
        new_cuboids = []
        for earlier in processed:
            int_cuboid = this_cuboid.get_intersection(earlier)
            if int_cuboid is not None:
                new_cuboids.append(int_cuboid)
        # We don't add any original cuboids with state == False to the processed list. We've already accounted
        # for where they intersect any other cuboids.
        if this_cuboid.state:
            processed.append(this_cuboid)
        processed.extend(new_cuboids)
    volume = functools.reduce(lambda a,b: a + b.volume(), processed, 0)
    return volume


def part_b(lines):
    return part_a(lines, just_50=False)
    

# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent, True)
