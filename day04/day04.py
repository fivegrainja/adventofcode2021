#! /usr/bin/env python3

import sys
from rich import print
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import aoc_utils
import itertools # https://docs.python.org/3/library/itertools.html

day = '04'
test_assertion_a = 4512
test_assertion_b = 1924

BOARD_SIZE = 5

def build_boards_and_results(lines):
    line_i = 2
    boards = []
    while line_i < len(lines):
        this_board = [int(p) for p in ' '.join(lines[line_i:line_i+BOARD_SIZE]).split()]
        boards.append(this_board)
        line_i += BOARD_SIZE + 1
    results = [[False] * len(b) for b in boards]
    return (boards, results)


def apply_pick(pick, board, board_results):
    """ Modify results to reflect pick
    """
    found_pick = False
    for num_i, num in enumerate(board):
        if num == pick:
            board_results[num_i] = True
            found_pick = True
    return found_pick


def check_board(board_results):
    """ Return True if board is a winner, false otherwise
    """
    # Check rows
    for i in range(0, BOARD_SIZE * ( BOARD_SIZE - 1 ), BOARD_SIZE):
        if all(board_results[i:i+BOARD_SIZE]):
            return True
    # Check cols
    for i in range(BOARD_SIZE):
        if all([board_results[j] for j in range(i,BOARD_SIZE * BOARD_SIZE, BOARD_SIZE)]):
            return True
    return False


def score_board(pick, board, board_results):
    sum = 0
    for i in range(len(board)):
        if not board_results[i]:
            sum += board[i]
    return pick * sum

    
def part_a(lines, find_last_winner=False):
    # Picks is a list of integer numbers to play on the boards
    picks = [int(s) for s in lines[0].split(',')]
    # Each board is a list of BOARD_SIZE*BOARD_SIZE integers
    # boards is a list of such boards
    # results has the same shape as boards, but stores booleans in each location indicating
    # if that board space has been picked
    boards, results = build_boards_and_results(lines)
    winners = set()
    for pick in picks:
        for board_i, board in enumerate(boards):
            # If we already identified this board as a winner don't process it any further
            if board_i in winners:
                continue
            found_pick = apply_pick(pick, board, results[board_i])
            if found_pick:
                if check_board(results[board_i]):
                    # Found a winner
                    if find_last_winner:
                        winners.add(board_i)
                        if len(winners) == len(boards):
                            return score_board(pick, board, results[board_i])
                    else:
                        return score_board(pick, board, results[board_i])
    raise Exception('No winner found')


def part_b(lines):
    return part_a(lines, find_last_winner=True)


aoc_utils.test_and_execute(part_a, day, test_assertion_a)
aoc_utils.test_and_execute(part_b, day, test_assertion_b)
