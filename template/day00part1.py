#! /usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

day = '00'
test_assertion = None

def do_the_thing(lines):
    return

aoc_utils.test_and_execute(do_the_thing, day, test_assertion)
