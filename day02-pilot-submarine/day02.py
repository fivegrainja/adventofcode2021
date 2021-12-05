#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

day = '02'
test_assertion_a = 150
test_assertion_b = 900

def part_a(lines):
    forward = 0
    depth = 0
    for line in lines:
        command, amount = line.split(' ')
        amount = int(amount)
        match command:
            case 'forward':
                forward += amount
            case 'down':
                depth += amount
            case 'up':
                depth -= amount
            case _:
                raise Exception(f'Unrecognized command {command}')
    print(f'{forward=}')
    print(f'{depth=}')
    return forward * depth

def part_b(lines):
    forward = 0
    depth = 0
    aim = 0
    for line in lines:
        command, amount = line.split(' ')
        amount = int(amount)
        match command:
            case 'forward':
                forward += amount
                depth += aim * amount
            case 'down':
                aim += amount
            case 'up':
                aim -= amount
            case _:
                raise Exception(f'Unrecognized command {command}')
    print(f'{forward=}')
    print(f'{depth=}')
    return forward * depth

aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
