#! /usr/bin/env python3

# See day16-questions.txt for context to this solution

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import functools

day = '16'
test_assertion_a = 31
test_assertion_b = 54


class BitStream:
    """ Encapsulates the stream of bits that are the packets.
    """

    def __init__(self, bits):
        self.bits = bits
        self.i = 0
        
    def take(self, n):
        """ Return a string with the next n bits from the stream, updating stream location
        """
        result =  self.bits[self.i:self.i+n]
        self.i += n
        return result
    
    def to_int(self, n):
        """ Take the next n bits from the stream and return them as an int
        """
        b = self.take(n)
        return int(b, 2)
    
    def has_more_packets(self):
        """ Return True if there are more packets in the stream, False otherwise.
        NB: The question wasn't entirely clear on this point, but this interpretation seems
        to work.
        """
        for c in self.bits[self.i:]:
            if c != '0':
                return True
        return False
    
    def __repr__(self):
        return f'i={self.i} len={len(self.bits)} {self.bits[self.i:self.i+10]}'


def operate(type_id, operands):
    """ Apply the operation specified in the type_id to the operands, returning the result
    """
    result = None
    match type_id:
        case 0: #sum
            result = sum(operands)
        case 1: # product
            result = functools.reduce(lambda x, y: x * y, operands, 1)
        case 2: # minimum
            result = min(operands)
        case 3: # maximum
            result = max(operands)
        # There is no case 4 because that is a literal
        case 5: # greater than
            assert(len(operands) == 2)
            result = 1 if operands[0] > operands[1] else 0
        case 6: # less than
            assert(len(operands) == 2)
            result = 1 if operands[0] < operands[1] else 0
        case 7: # equal
            assert(len(operands) == 2)
            result = 1 if operands[0] == operands[1] else 0
        case _:
            raise Exception(f'Unrecognized type_id {type_id}')
    return result


def read_packet(bit_stream):
    """ Read the next packet from bit_stream, including all sub-packets.
    Return (versions_sum, op_result) where versions_sum is the sum of all packet versions encountered
    (part a solution) and op_result is the numeric result of the operation specified by the packet and
    sub packets.
    """
    version = bit_stream.to_int(3)
    type_id = bit_stream.to_int(3)
    versions_sum = version
    op_result = None
    if type_id == 4:
        # Packet is literal value
        literal_bits = ''
        while True:
            # Read chunks 5 bits at a time, ending with the first one that starts with 0
            bits = bit_stream.take(5)
            literal_bits += bits[1:]
            if bits[0] == '0':
                break
        literal = int(literal_bits, 2)
        op_result = literal
    else:
        # Operation packet
        length_type_id = bit_stream.take(1)
        if length_type_id == '0':
            # We have a fixed number of bits that are the sub packets. Created a dedicated
            # sub_bit_stream with these bits and process it recursively.
            num_bits = bit_stream.to_int(15)
            subpacket = bit_stream.take(num_bits)
            sub_bit_stream = BitStream(subpacket)
            operands = []
            while sub_bit_stream.has_more_packets():
                sub_versions_sum, sub_op_result = read_packet(sub_bit_stream)
                versions_sum += sub_versions_sum
                operands.append(sub_op_result)
            op_result = operate(type_id, operands)
        elif length_type_id == '1':
            # We have a specified number of sub packets.
            num_sub_packets = bit_stream.to_int(11)
            operands = []
            for i in range(num_sub_packets):
                sub_versions_sum, sub_op_result = read_packet(bit_stream)
                versions_sum += sub_versions_sum
                operands.append(sub_op_result)
            op_result = operate(type_id, operands)
        else:
            raise Exception(f'Unknown {length_type_id=}')
    return versions_sum, op_result


def part_a(lines):
    """ Return the sum of the version of all packets encountered
    """
    bits = ''.join([bin(int(c, 16))[2:].rjust(4, '0') for c in lines[0]])
    bit_stream = BitStream(bits)
    version_sum, op_result = read_packet(bit_stream)
    return version_sum


def part_b(lines):
    """ Return the result of the operation specified in the packet and sub packets
    """
    bits = ''.join([bin(int(c, 16))[2:].rjust(4, '0') for c in lines[0]])
    bit_stream = BitStream(bits)
    version_sub, op_result = read_packet(bit_stream)
    return op_result


# test_and_execute is a utility function that runs the function with the correct input, checks that the 
# output for the test data is the expected value, prints time it took to run, etc.
aoc_utils.test_and_execute(part_a, day, test_assertion_a, Path(__file__).parent)
aoc_utils.test_and_execute(part_b, day, test_assertion_b, Path(__file__).parent)
