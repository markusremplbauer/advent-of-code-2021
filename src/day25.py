# Advent of Code 2021, Day 25
# markusremplbauer

from itertools import count

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls

# identifies '.', '>', 'v'
FREE, EAST, SOUTH = 0, 1, 2


@print_calls
def part1(grid):
    for i in count(1):
        n1 = move_sea_cuke(grid, EAST)
        n2 = move_sea_cuke(grid, SOUTH)

        # stop if no sea cuke moved
        if n1 + n2 == 0:
            return i


def move_sea_cuke(grid, sea_cuke):
    lookahead = east if sea_cuke == EAST else south
    moves = []

    # check if the sea cuke can move
    for xy, val in np.ndenumerate(grid):
        if val == sea_cuke:
            px, py = lookahead(*xy, grid.shape)
            if grid[px, py] == FREE:
                moves.append((*xy, px, py))

    # perform the moves
    for x, y, px, py in moves:
        grid[x, y] = FREE
        grid[px, py] = sea_cuke

    return len(moves)


def east(x, y, shape):
    return x, (y + 1) % shape[1]


def south(x, y, shape):
    return (x + 1) % shape[0], y


def load(data):
    data = data.replace(".", "0").replace(">", "1").replace("v", "2")
    return np.fromiter(data.replace("\n", ""), dtype=int).reshape(-1, data.index("\n"))


def main():
    puzzle = Puzzle(year=2021, day=25)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1


if __name__ == "__main__":
    main()
