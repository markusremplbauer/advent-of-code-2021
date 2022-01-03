# Advent of Code 2021, Day 07
# markusremplbauer

import numpy as np
from aocd.models import Puzzle
from funcy import lmap, print_calls


@print_calls
def part1(data):
    return solve(data)


@print_calls
def part2(data):
    return solve(data, gauss=True)


def solve(data, gauss=False):
    min_coast = np.inf
    for p in range(max(data)):
        if gauss:
            min_coast = min(sum(gauss_sum(abs(p - x)) for x in data), min_coast)
        else:
            min_coast = min(sum(abs(p - x) for x in data), min_coast)

    return min_coast


def gauss_sum(n):
    return int((n * (n + 1)) / 2)


def load(data):
    return lmap(int, data.split(","))


def main():
    puzzle = Puzzle(year=2021, day=7)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
