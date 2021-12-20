#! /usr/bin/env python3

# See day<number>-questions.txt for context to this solution

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import functools
import itertools

day = '18'
test_assertion_a = None
test_assertion_b = None

class Node:

    def __init__(self, snailfish_number=None):
        self.left = None
        self.right = None
        self.value = None
        if snailfish_number is not None:
            if snailfish_number.startswith('['):
                left, right = Node.split_pair(snailfish_number)
                self.left = Node(left)
                self.right = Node(right)
            else:
                self.value = int(snailfish_number)
    
    def reduce(self):
        while True:
            # print(f'Reduce {self}')
            # print('looping in reduce')
            if self.explode():
                continue
            # print('Got past the explode')
            if self.split():
                continue
            break
    
    @staticmethod
    def split_pair(snailfish_number):
        assert(snailfish_number[0] == '[')
        assert(snailfish_number[-1] == ']')
        num_opens = 0
        for i in range(1, len(snailfish_number)):
            c = snailfish_number[i]
            if c == ',' and num_opens == 0:
                return (snailfish_number[1:i], snailfish_number[i+1:-1])
            elif c == '[':
                num_opens += 1
            elif c == ']':
                num_opens -= 1
        raise Exception(f'Did not find split for {snailfish_number=}')

    def __repr__(self):
        if self.is_regular():
            return str(self.value)
        return f'[{self.left},{self.right}]'
    
    def __add__(self, other):
        # print(f'__add__ {self=} {other=}')
        sum = Node(f'[{self},{other}]')
        sum.reduce()
        return sum
    
    def __eq__(self, other):
        # Arguably we should be comparing reduced versions of self and other
        return str(self) == str(other)

    def is_regular(self):
        if self.value is None:
            assert(self.left is not None)
            assert(self.right is not None)
            return False
        assert(self.left is None)
        assert(self.right is None)
        return True
    
    def explode(self):
        """ Find the leftmost nested pair at depth >= 4 and explode it.
        """
        # Directly from the problem:
        # To explode a pair, the pair's left value is added to the first regular
        # number to the left of the exploding pair (if any), and the pair's
        # right value is added to the first regular number to the right of the
        # exploding pair (if any). Exploding pairs will always consist of two
        # regular numbers. Then, the entire exploding pair is replaced with the
        # regular number 0.
        queue = [(self, 1)]
        last_regular_node = None
        explode_right_value = None
        any_changes = False
        while queue:
            node, level = queue.pop()
            # print(f'Popped {node} at level {level}')
            # if len(queue) > 10:
            #     sys.exit()
            # If this is a regular number then save it for use in the explode operation
            if node.is_regular():
                # print(f'Found regular number {node.value}')
                if explode_right_value is not None:
                    # print(f'assigning it the value for the right')
                    node.value += explode_right_value
                    # Already set any_changes when we exploded
                    break
                # print(f'recording it for last reg left')
                last_regular_node = node
            elif explode_right_value is None and level > 4 and node.left.is_regular() and node.right.is_regular():
                # print(f'Found a pair to explode {node.left.value},{node.right.value}')
                # Time to explode
                if last_regular_node is not None:
                    # print(f'{last_regular_node=}')
                    last_regular_node.value += node.left.value
                    last_regular_node = None # Not necessary, just tidy
                explode_right_value = node.right.value
                # print(f'{explode_right_value=}')
                node.left = None
                node.right = None
                node.value = 0
                any_changes = True
            else:
                # Push both children onto the queue, right then left (so left will be prioritiezed)
                # print(f'Pushing {node.left} and {node.right}')
                queue.append((node.right, level + 1))
                queue.append((node.left, level + 1))
            # sys.exit()
        return any_changes
    
    def split(self):
        queue = [self]
        while queue:
            node = queue.pop()
            if node.is_regular():
                if node.value >= 10:
                    # Split this node
                    # print(f'Splitting {node.value}')
                    left = node.value // 2
                    right = node.value - left
                    node.left = Node(str(left))
                    node.right = Node(str(right))
                    node.value = None
                    return True
            else:
                queue.append(node.right)
                queue.append(node.left)
        return False
    
    def magnitude(self):
        if self.is_regular():
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        
def part_a(lines):
    # nums = [int(l) for l in lines if l != '']
    return

def part_b(lines):
    # nums = [int(l) for l in lines if l != '']
    return




for input, expected in [
# ("""[1,1]
# [2,2]
# [3,3]
# [4,4]""".split(),
# '[[[[1,1],[2,2]],[3,3]],[4,4]]'),
("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""".split(),
'[[[[3,0],[5,3]],[4,4]],[5,5]]')
]:
    nodes = [Node(line.strip()) for line in input if line.strip()]
    # print(nodes)
    sum = functools.reduce(lambda a,b:a+b, nodes)
    # print(f'{sum=} {expected=}')
    assert(str(sum) == str(expected))


for input, output in (
    ('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
    ('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'),
    ('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
    ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'),
    ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')
):
    # print()
    # print(f'Testing {input=} {output=}')
    node = Node(input)
    node.explode()
    # print(f'Result {input=} {output=} {str(node)=}')
    assert(str(node) == output)

for input, output in (
    ('[10,8]', '[[5,5],8]'),
    ('[4,[8,11]]', '[4,[8,[5,6]]]')
):
    # print()
    # print(f'Testing {input=} {output=}')
    node = Node(input)
    node.split()
    # print(f'Result {input=} {output=} {str(node)=}')
    assert(str(node) == output)

# print('summing')
sum = Node('1') + Node('2') + Node('3')
# print(f'{sum=}')

sum = functools.reduce(lambda a, b: a + b, (Node('[1,1]'), Node('[2,2]'), Node('[3,3]'),Node('[4,4]')))
# print(f'{sum=}')
assert(str(sum) == '[[[[1,1],[2,2]],[3,3]],[4,4]]')

sum = Node('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]') + Node('[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]')
# print(sum)
# print('[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]')


input = [
    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
    '[7,[5,[[3,8],[1,4]]]]',
    '[[2,[2,2]],[8,[8,1]]]',
    '[2,9]',
    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
    '[[[5,[7,4]],7],1]',
    '[[[[4,2],2],6],[8,7]]']
nodes = [Node(i) for i in input]
sum = nodes[0]
for other in nodes[1:]:
    new_sum = sum + other
    # print(f'{sum} + {other} = {new_sum}')
    sum = new_sum


# sum = functools.reduce(lambda a,b: a+b, nodes)
assert(str(sum) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')


input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split()
nodes = [Node(line.strip()) for line in input if line.strip()]
sum = functools.reduce(lambda a,b:a+b, nodes)
expected = '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
# print(f'{sum=} {expected=}')
assert(str(sum) == str(expected))
# print(f'{sum.magnitude()=}')
assert(sum.magnitude() == 4140)

print('PART A')
path = Path(__file__).parent / 'day18-input.txt'
with path.open('r') as f:
    lines = f.readlines()
nodes = [Node(line.strip()) for line in lines if line.strip()]
sum = functools.reduce(lambda a,b:a+b, nodes)
print(f'{sum.magnitude()=}')

print('PART B')
max_magnitude = 0
for a, b in itertools.permutations(nodes, 2):
    sum = a + b
    mag = sum.magnitude()
    max_magnitude = max(max_magnitude, mag)
print(f'Max magnitude is {max_magnitude}')


print('DONE')


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
# aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
# aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
