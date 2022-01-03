# Advent of Code 2021, Day 01
# markusremplbauer

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(data):
    return (np.diff(data) > 0).sum()


@print_calls
def part2(data):
    window = [x + y + z for x, y, z in zip(data, data[1:], data[2:])]

    return (np.diff(window) > 0).sum()


def load(data):
    return np.fromstring(data, dtype=int, sep="\n")


def main():
    puzzle = Puzzle(year=2021, day=1)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
