#! /usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import itertools # https://docs.python.org/3/library/itertools.html

day = '11'
test_assertion_a = 1656
test_assertion_b = 195

# For part A, the number of steps we iterate through
NUM_STEPS = 100

# The energy level at which an octo flashes
FLASH_ENERGY = 10

class Qctopus:
    """ Represents a single octopus within the grid. Maintains its energy state and has a list of neighbors
    which it will notify when it flashes.
    """

    def __init__(self, energy):
        self.energy = energy
        self.flashes = 0
        self.flashed_this_step = False
        self.neighbors = []
    
    def start_step_and_add_energy(self):
        """ Start a new step by incrementing energy by one.
        """
        self.flashed_this_step = False
        self.energy += 1
    
    def think_about_flashing(self, neighbor_just_flashed):
        """ Check energy level and maybe flash, first incrementing energy by one if neighbor_just_flashed.
        """
        # If octo already flashed this step then do nothing
        if not self.flashed_this_step:
            if neighbor_just_flashed:
                self.energy += 1
            if self.energy >= FLASH_ENERGY:
                self.flash()
    
    def flash(self):
        """ Flash, which increments the flash count, sets energy to zero and notifies neighbors
        """
        self.flashes += 1
        self.flashed_this_step = True
        self.energy = 0
        for n in self.neighbors:
            n.think_about_flashing(True)

    
class OctoGrid:
    """ Represents the grid of octos
    """

    def __init__(self, energies):
        self.octos = []
        # Create 2D array of octos
        for row_i, row in enumerate(energies):
            self.octos.append([])
            for col_i, energy in enumerate(row):
                self.octos[-1].append(Qctopus(energy))
        # Set all the neighbors
        for row_i, row in enumerate(self.octos):
            for col_i, octo in enumerate(row):
                if row_i > 0:
                    octo.neighbors += self.octos[row_i - 1][max(0, col_i - 1):col_i + 2]
                if row_i < len(self.octos) - 1:
                    octo.neighbors += self.octos[row_i + 1][max(0, col_i - 1):col_i + 2]
                if col_i > 0:
                    octo.neighbors.append(self.octos[row_i][col_i - 1])
                if col_i < len(self.octos[row_i]) - 1:
                    octo.neighbors.append(self.octos[row_i][col_i + 1])
            
    def do_step(self):
        """ Perform a step across all the octos in the grid.
        There are two parts to each step - increment an octo's energy, then check to see if it should flash. But
        we need to increment the energy of all octos before any of them decide to flash and affect their neighbors.
        """
        for octo in itertools.chain(*self.octos):
            octo.start_step_and_add_energy()
        for octo in itertools.chain(*self.octos):
            octo.think_about_flashing(False)
    
    def count_flashes(self):
        """ Return sum of flashes of all octos
        """
        count = 0
        for octo in itertools.chain(*self.octos):
            count += octo.flashes
        return count
    
    def did_they_all_flash(self):
        """ Return True if all octos in the grid flashed last step, False if not.
        If an octo flashed its energy will be 0
        """
        return not any([o.energy for o in itertools.chain(*self.octos)])
    

def part_a(lines):
    """ Return the total number of flashes after NUM_STEPS
    """
    energies = [[int(n) for n in line] for line in lines]
    grid = OctoGrid(energies)
    for day in range(NUM_STEPS):
        grid.do_step()
    return grid.count_flashes()


def part_b(lines):
    """ Return the number of the first step where all octos flashed in the same step
    """
    energies = [[int(n) for n in line] for line in lines]
    grid = OctoGrid(energies)
    day = 0
    while True:
        grid.do_step()
        day += 1
        if grid.did_they_all_flash():
            break
    return day

# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
