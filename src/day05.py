# Advent of Code 2021, Day 05
# markusremplbauer

import numpy as np
from aocd.models import Puzzle
from dotmap import DotMap
from funcy import print_calls
from parse import parse


@print_calls
def part1(data):
    return solve(data, only_orthogonal=True)


@print_calls
def part2(data):
    return solve(data)


def solve(data, only_orthogonal=False):
    size = max(max(row.values()) for row in data) + 1
    board = np.zeros((size, size), dtype=int)
    for row in data:
        if row.x1 == row.x2 or row.y1 == row.y2:
            for x, y in get_orthogonal_indices(*row.values()):
                board[y, x] += 1
        elif not only_orthogonal:
            for x, y in get_diagonal_indices(*row.values()):
                board[y, x] += 1

    return len(board[board >= 2])


def get_orthogonal_indices(x1, y1, x2, y2):
    v_x = 0 if x1 == x2 else (1 if x1 < x2 else -1)
    v_y = 0 if y1 == y2 else (1 if y1 < y2 else -1)

    size = max(abs(x2 - x1), abs(y2 - y1)) + 1
    for i in range(size):
        yield x1 + i * v_x, y1 + i * v_y


def get_diagonal_indices(x1, y1, x2, y2):
    v_x = 1 if x1 < x2 else -1
    v_y = 1 if y1 < y2 else -1

    for i in range(abs(x2 - x1) + 1):
        yield x1 + i * v_x, y1 + i * v_y


def load(data):
    return [
        DotMap(parse("{x1:d},{y1:d} -> {x2:d},{y2:d}", line).named)
        for line in data.split("\n")
    ]


def main():
    puzzle = Puzzle(year=2021, day=5)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
