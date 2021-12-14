#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

day = '10'
test_assertion_a = 26397
test_assertion_b = 288957

# pairs represents the correct closing character for each opening character.
pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

# Part B scoring
# Note that the question phrases this scoring in terms of the closing characters that would be needed.
# However, what we have is a stack of the corresponding opening characters, so the keys in the dict
# below are those corresponding opening characters instead of the closing ones.
completion_scoring = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

def assess_line(line):
    """ Return (is_line_valid, result)
    is_line_valid is False if there is an invalid closing character, and result is the invalid closing character
    is_line_valid is True if line is complete or incomplete, and result is the stack of unclosed opening characters (if any)
    with the most recent on top.
    """
    stack = []
    for c in line:
        if c in '([{<':
            stack.append(c)
        elif c in ')]}>':
            opening = stack.pop()
            if pairs[opening] != c:
                return (False, c)
        else:
            raise Exception('Unknown character')
    return (True, stack)


def score_illegals(illegals):
    """ Take a list of illegal closing characters and return a score per the question's criteria
    """
    sum = illegals.count(')') * 3
    sum += illegals.count(']') * 57
    sum += illegals.count('}') * 1197
    sum += illegals.count('>') * 25137
    return sum


def score_completion(stack):
    """ Take the stack from an incomplete line and return the score of the characters needed to close it.
    """
    score = 0
    while stack:
        score *= 5
        c = stack.pop()
        score += completion_scoring[c]
    return score

            
def part_a(lines):
    """ For each line, push opening characters onto a stack. When we find a closing character if it matches the top one on the
    stack then pop that opening one off the stack. If it isn't a match then we have an invalid closing character.
    """
    illegals = []
    for line in lines:
        is_line_valid, invalid_character = assess_line(line)
        if not is_line_valid:
            illegals.append(invalid_character)
    return score_illegals(illegals)


def part_b(lines):
    """ For each valid line consider the stack of opening characters that didn't get closed.
    Compute a score for each line per the question, then return the median value of these scores.
    """
    scores = []
    for line in lines:
        is_line_valid, stack = assess_line(line)
        if is_line_valid:
            scores.append(score_completion(stack))
    scores.sort()
    return scores[len(scores) // 2]


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
