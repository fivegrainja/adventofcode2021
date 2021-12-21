#! /usr/bin/env python3

# See day21-questions.txt for context to this solution

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

import itertools
import more_itertools
import functools

day = '21'
test_assertion_a = 739785
test_assertion_b = 444356092776315


def part_a(lines):
    """ Play the game until one score reaches 1000 or greater. Return the loosing score times the
    number of times the die was rolled.
    """
    a_pos = int(lines[0].split()[-1])
    b_pos = int(lines[1].split()[-1])
    a_score = b_score = 0
    die = itertools.cycle(range(1, 101)) # Iterator that repeats 1..100
    turn = 0
    while a_score < 1000 and b_score < 1000:
        turn += 1
        rolls = more_itertools.take(3, die)
        n = sum(rolls) % 10
        if turn % 2 == 1:
            a_pos += n
            if a_pos > 10:
                a_pos -= 10
            a_score += a_pos
        else:
            b_pos += n
            if b_pos > 10:
                b_pos -= 10
            b_score += b_pos
    return min(a_score, b_score) * (turn * 3) # We roll the die 3 times each turn


@functools.cache
def better_count_wins(this_pos, other_pos, this_score, other_score):
    """ Given the positions and scores of both players, return the number of wins possible
    for each - (wins by this_ player, wins by other_ player)
    """
    # Strategy: For any given player's turn do the following:
    #   Figure out the list of possible 3-roll combinations
    #   For each of these cobinations:
    #       Calculate the player's new score
    #       If that score results in a win, increment the players win count
    #       Otherwise recursively call function with new score/position, but flipping
    #         the this_, other_ roles to make it the other player's turn, and adding the wins
    #         returned from that situation to the wins we are accumulating for all possible rolls.
    #   Return the total wins for the two players that are possible from the conditions
    #     described by the arguments to this function.  
    this_wins = 0
    other_wins = 0
    rolls = itertools.product((1, 2, 3), repeat=3)
    for roll in rolls:
        n = sum(roll)
        new_this_pos = this_pos + n
        if new_this_pos > 10:
            new_this_pos -= 10
        new_this_score = this_score + new_this_pos
        if new_this_score >= 21:
            this_wins += 1
        else:
            more_other, more_this = better_count_wins(other_pos, new_this_pos, other_score, new_this_score)
            this_wins += more_this
            other_wins += more_other
    return this_wins, other_wins


def part_b(lines):
    a_pos = int(lines[0].split()[-1])
    b_pos = int(lines[1].split()[-1])
    a, b = better_count_wins(a_pos, b_pos, 0, 0)
    return max(a, b)

# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
