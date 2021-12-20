#! /usr/bin/env python3

# See day20-questions.txt for context to this solution

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils

day = '20'
test_assertion_a = 35
test_assertion_b = 3351

class Image:

    def __init__(self, algo, image_lines, padding):
        """ Initialize image with data in image_lines and pad each edge with padding
        extra rows/columns.
        """
        self.algo = algo
        # actual_dim tracks the size of the actual data within the grid that we care about.
        self.actual_dim = len(image_lines)
        # image is the data from image_lines surrounded by padding
        dim = len(image_lines) + 2 * padding
        self.image = [['.'] * dim for i in range(padding)]
        for row in image_lines:
            self.image.append(['.'] * padding + [c for c in row] + ['.'] * padding)
        self.image.extend([['.'] * dim for i in range(padding)])
    
    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.image])
    
    def enhance(self):
        """ Apply the image enhancement algorithm to the image.
        """
        old_dim = len(self.image)
        new_dim = old_dim
        new_image = [['.'] * new_dim for i in range(new_dim)]
        for y in range(1, old_dim - 1):
            for x in range(1, old_dim - 1):
                neighbors = self.image[y - 1][x - 1:x + 2]
                neighbors += self.image[y][x - 1:x + 2]
                neighbors += self.image[y + 1][x - 1:x + 2]
                bits = ''.join(['1' if n == '#' else '0' for n in neighbors])
                algo_i = int(bits, 2)
                new_image[y][x] = self.algo[algo_i]
        self.actual_dim += 2
        self.image = new_image
    
    def count_lit_bits(self):
        r0 = 0
        origin = (len(self.image) - self.actual_dim) // 2
        for row_i in range(origin, origin + self.actual_dim):
            for col_i in range(origin, origin + self.actual_dim):
                if self.image[row_i][col_i] == '#':
                    r0 += 1
        return r0
    

def part_a(lines, n=2):
    image = Image(lines[0], lines[2:], n * 2)
    for i in range(n):
        image.enhance()
    return image.count_lit_bits()


def part_b(lines):
    return part_a(lines, n=50)


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
