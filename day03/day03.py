#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import operator

day = '03'
test_assertion_a = 198
test_assertion_b = 230

def part_a(lines):
    num_bits = len(lines[0])
    num_lines = len(lines)
    bits = [[line[i] for line in lines] for i in range(num_bits)]
    gamma = ['1' if bits[i].count('1') > (num_lines/2) else '0' for i in range(num_bits)]
    epsilon = ['0' if bit == '1' else '1' for bit in gamma]
    g = int(''.join(gamma), 2)
    e = int(''.join(epsilon), 2)
    return g * e

def part_b(lines):
    num_bits = len(lines[0])
    product = 1
    for op in (operator.ge, operator.lt):
        element = set(lines)
        for i in range(num_bits):
            chosen = '1' if op([e[i] for e in element].count('1'), len(element) / 2) else '0'
            element = set([e for e in element if e[i] == chosen])
            if len(element) == 1:
                break
        else:
            raise Exception('We got through the set of elements without finding a unique match')
        product *= int(element.pop(), 2)
    return product
  

aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
