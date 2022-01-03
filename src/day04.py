# Advent of Code 2021, Day 04
# markusremplbauer

import numpy as np
import numpy.ma as ma
from aocd.models import Puzzle
from funcy import lmap, print_calls

BOARD_SHAPE = 5


@print_calls
def part1(draws, boards):
    return bingo(draws, boards)


@print_calls
def part2(draws, boards):
    return bingo(draws, boards, last_winner=True)


def bingo(draws, boards, last_winner=False):
    num_boards = len(boards)
    masks = [np.zeros_like(boards[0], dtype=bool) for _ in range(num_boards)]
    winners = []

    draw = None
    for draw in draws:
        for i in range(num_boards):
            masks[i] = mask_board(boards[i], masks[i], draw)

        for i in range(num_boards):
            if i not in winners and has_won(masks[i]):
                winners.append(i)

                if not last_winner:
                    return score(boards[i], masks[i], draw)

        if len(winners) == num_boards:
            break

    last = winners[-1]
    return score(boards[last], masks[last], draw)


def mask_board(board, mask, draw):
    return np.logical_or(mask, (board == draw))


def has_won(mask):
    col = any(mask.sum(axis=0) == BOARD_SHAPE)
    row = any(mask.sum(axis=1) == BOARD_SHAPE)
    return col or row


def score(board, mask, draw):
    mb = ma.masked_array(board, mask)
    return mb.sum() * draw


def load(data):
    lines = data.splitlines()
    draws = lmap(int, lines[0].split(","))
    boards = []
    for i in range(2, len(lines), BOARD_SHAPE + 1):
        board = lines[i : (i + BOARD_SHAPE)]
        board = [lmap(int, row.split()) for row in board]
        boards.append(np.array(board, dtype=int))

    return draws, boards


def main():
    puzzle = Puzzle(year=2021, day=4)

    ans1 = part1(*load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(*load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
