#! /usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

import collections # https://docs.python.org/3/library/collections.html
import itertools # https://docs.python.org/3/library/itertools.html

day = '08'
test_assertion_a = 26
test_assertion_b = 61229

# Wires per digit represents what wires will be active for each digit
wires_per_digit= {
    '0': 'abcefg',
    '1': 'cf',
    '2': 'acdeg',
    '3': 'acdfg',
    '4': 'bcdf',
    '5': 'abdfg',
    '6': 'abdefg',
    '7': 'acf',
    '8': 'abcdefg',
    '9': 'abcdfg'
}

# digit_for_wires is the inverse of wires_per_digit (above.) For a given set of wires
# (alphabetical order) what is the digit they represent.
digit_for_wires= { v:k for k, v in wires_per_digit.items()}

# These are the digits that have a unique number of segments, so we can tell just from the
# number of segments which digit is represented
digits_by_length = {
    2: 1,   # If you have exactly two segments then that represents the digit 1
    3: 7,   # If you have exactly three segments then that represents the digit 7 ...
    4: 4,
    7: 8
}


def process_known_pattern(pattern, digit, wires_to_segments):
    """ We know that the pattern represents the segments in digit. Update wires_to_segments
    to represent this.
    """
    digit_wires = wires_per_digit[digit]
    for wire in 'abcdefg':
        if wire in digit_wires:
            # This wire is hooked up to one of the one of the segments in the given pattern
            wires_to_segments[wire] &= set(pattern)
        else:
            # This wire is not hooked up to any of the segments in the given pattern
            wires_to_segments[wire] -= set(pattern)


def part_a(lines):
    """ Return the number of known digits (the easily identified ones from digits_by_length)
    that exist in all the outputs.
    """
    known_count = 0
    for line in lines:
        p1, p2 = line.split('|')
        patterns = p1.split()
        outputs = p2.split()
        known_count += len([len_o for o in outputs if (len_o:=len(o) in digits_by_length)])
    return known_count


def part_b(lines):
    """ Decipher the output on each line and return the sum of all the outputs.

    Strategy
    For each input line start with a mapping of wires to possible segments each is 
    connected to. To start with each wire could be mapped to any of the 7 segments.
    We proceed through several stages to narrow this down to just one possible segment
    for each wire. This mapping of wires to segments is wires_to_segments

    Step 1 - Start with the digits we can identify based soley on number of segments. For example
    the digit 1 is the only digit represented by just two segments. Find the input pattern that
    has just two segments. We now that wires c and f map to those two segments (though we don't
    know which is which yet.) In wires_to_segments we can narrow down wires c and f to just have
    those two segments as options, and remove those two segments as options from all other wires.
    Do this with the other digits with unique segment counts - 7, 4 and 8

    Step 2 - Consider the digits comprised of 5 segments - 2, 3 and 5. Observe that
    wire b is only active for one of those digits
    wire e is only active for one of those digits
    Identify the segments that show up in only one of the 5-segment patterns. Narrow the options
    for wire b and e to those segments and remove those segments from the options for other wires.
    Refine wires_to_segments to reflect this.

    Step 3 - Similar to above, but with the 6 segment digits - 0, 6 and 9
    wire c will be on for 2 of those digits
    wire f will be on for 3 of those digits
    Further refine wires_to_segments again

    Step 4 - Steps 2 and 3 will result is more wires for which there is only one possible segment. For each of these
    remove that segment from the list of possible segments for any other wires.

    At this point wires_to_segments will have one possible segment for each wire. By using this mapping in reverse
    we can translate the digits in the output, create an integer from them, and sum them.
    """
    sum = 0
    for line in lines:
        p1, p2 = line.split('|')
        # Patterns is a list of strings from the first part of the input line
        patterns = p1.split()
        # Outputs is a list of strings from the second part of the input line
        outputs = p2.split()

        patterns.sort(key=len)
        # Now that patterns is sorted by length we know that
        # pattern[0] (len 2) -> digit 1 -> wires cf
        # pattern[1] (len 3) -> digit 7 -> wires acf
        # pattern[2] (len 4) -> digit 4 -> wires bcdf
        # pattern[3:6] (len 5) -> digits 2, 3, 5
        # pattern[6:9] (len 6) -> digits 0, 6, 9
        # pattern[9] (len 8) -> digit 8 -> wires abcdefg

        # wires_to_segments keeps track of which segments a given wire might be hooked up to. As we process our
        # input we start narrowing down the segments that each wire might be hooked to until we have only one
        # option for each wire.
        wires_to_segments = {c:set('abcdefg') for c in 'abcdefg'}
        # Process the unique patterns from above for digits 1, 4, 7, 8
        process_known_pattern(patterns[0], '1', wires_to_segments)
        process_known_pattern(patterns[1], '7', wires_to_segments)
        process_known_pattern(patterns[2], '4', wires_to_segments)
        process_known_pattern(patterns[9], '8', wires_to_segments)

        # Now it gets a bit harder. Looking at the digits that have 5 segments there is some
        # useful info
        # 5 segment patterns: 2, 3, 5
        #   Only 5 has wire b
        #   Only 2 has wire e
        # Put another way
        #   b will occur once
        #   e will occur once
        five_segment_patterns = [p for p in patterns if len(p) == 5]
        counter = collections.Counter(itertools.chain(*five_segment_patterns))
        occurring_once_in_len5_patterns = set([segment for segment in counter if counter[segment] == 1])
        # &= means take the intersection of the two sets and assign to set on the left
        wires_to_segments['b'] &= occurring_once_in_len5_patterns
        wires_to_segments['e'] &= occurring_once_in_len5_patterns

        # Looking at digits with 6 segments: 0, 6, 9
        # wire c will be on for 2 of those
        # wire f will be on for 3 of those
        six_segment_patterns = [p for p in patterns if len(p) == 6]
        counter = collections.Counter(itertools.chain(*six_segment_patterns))
        occurring_twice_in_len6_patterns = set([segment for segment in counter if counter[segment] == 2])
        wires_to_segments['c'] &= occurring_twice_in_len6_patterns
        occurring_thrice_in_len6_patterns = set([segment for segment in counter if counter[segment] == 3])
        wires_to_segments['f'] &= occurring_thrice_in_len6_patterns

        # For any wire that maps to only a single segment, remove the option for any other
        # wires to be mapped to that segment
        for wire, segments in wires_to_segments.items():
            if len(segments) == 1:
                # No other wire can be hooked up to this segment
                for other_wire in wires_to_segments:
                    if other_wire != wire:
                        wires_to_segments[other_wire] -= segments

        # Our mapping should be 1-1 now, check
        for wire, segments in wires_to_segments.items():
            if len(segments) != 1:
                raise Exception('Did not determine unique mapping for wires_to_segments')
      
        # Create the reverse mapping from wires_to_segments - from segments to wires
        segments_to_wires = {str(v.pop()):k for k,v in wires_to_segments.items()}
        # Convert each digit in the output to the actual, unscrambled digit it represents
        o_digits = []
        for o in outputs:
            # o_wires is the wires that map to the segments in this output digit
            o_wires = [segments_to_wires[s] for s in o]
            # Lookup the digit these wires represent. The key into digit_for_wires is a sorted str
            # And append this digit to o_digits list.
            o_wires_key = ''.join(sorted(o_wires))
            o_digits.append(digit_for_wires[o_wires_key])
        num = int(''.join(o_digits))
        sum += num
    
    return sum
    

aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
