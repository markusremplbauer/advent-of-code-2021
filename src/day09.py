# Advent of Code 2021, Day 09
# markusremplbauer

from itertools import product

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(data):
    risk_levels, _ = solve(data)
    return sum(risk_levels)


@print_calls
def part2(data):
    _, basins = solve(data)
    return np.prod(sorted(basins, reverse=True)[:3])


def solve(data):
    risk_levels = []
    basins = []
    for x, y in product(range(data.shape[0]), range(data.shape[1])):
        if is_low_point(x, y, data):
            risk_levels.append(data[x, y] + 1)
            basins.append(len(basin(x, y, data)))

    return risk_levels, basins


def basin(x, y, data):
    coords = [(x, y)]
    for adj in adjacent(x, y, data.shape):
        if data[x, y] < data[adj] < 9:
            cs = basin(*adj, data)
            for c in cs:
                if c not in coords:
                    coords.append(c)
    return coords


def is_low_point(x, y, data):
    return data[x, y] < min(data[adj] for adj in adjacent(x, y, data.shape))


def adjacent(x, y, shape):
    """
    Returns the adjacent coordinates without diagonals and with out-of-bounds check.
    """
    adj = (
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y),
    )
    return [(x, y) for x, y in adj if 0 <= x < shape[0] and 0 <= y < shape[1]]


def load(data):
    return np.fromiter(data.replace("\n", ""), dtype=int).reshape(-1, data.index("\n"))


def main():
    puzzle = Puzzle(year=2021, day=9)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
