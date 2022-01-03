# Advent of Code 2021, Day 11
# markusremplbauer

from itertools import count

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(data):
    return solve(data, limit=100)


@print_calls
def part2(data):
    return solve(data)


def solve(data, limit=None):
    total_flashes = 0
    steps = range(limit) if limit else count()
    for step in steps:
        data += 1

        # positions to be flashed
        overflow = set(map(tuple, np.argwhere(data > 9)))
        flashed = set()

        while overflow:
            flash = overflow.pop()
            flashed.add(flash)

            # update adjacent positions
            for adj in adjacent(*flash, shape=data.shape):
                if adj not in flashed:
                    data[adj] += 1

                    # add to overflow if flashed
                    if data[adj] > 9:
                        overflow.add(adj)

        total_flashes += len(flashed)

        # reset flashed positions
        for adj in flashed:
            data[adj] = 0

        # no limit: return step at which flashes are synchronized
        if limit is None and len(flashed) == data.size:
            return step + 1

    # limit: return the amount of total flashes
    return total_flashes


def adjacent(x, y, shape):
    """
    Returns the adjacent coordinates with diagonal and out-of-bounds check.
    """
    adj = (
        (x, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y),
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
    )
    return ((x, y) for x, y in adj if 0 <= x < shape[0] and 0 <= y < shape[1])


def load(data):
    return np.fromiter(data.replace("\n", ""), dtype=int).reshape(-1, data.index("\n"))


def main():
    puzzle = Puzzle(year=2021, day=11)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
