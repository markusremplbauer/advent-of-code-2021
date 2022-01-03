# Advent of Code 2021, Day 15
# markusremplbauer

from itertools import product

import networkx as nx
import numpy as np
from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(data):
    return solve(data)


@print_calls
def part2(data):
    return solve(extend_grid(data, 5))


def solve(data):
    graph = nx.grid_2d_graph(*data.shape)

    end = data.shape[0] - 1, data.shape[1] - 1

    p = nx.shortest_path(
        graph, source=(0, 0), target=end, weight=lambda u, v, d: data[v]
    )

    return sum(data[(x, y)] for x, y in p[1:])


def extend_grid(tile, n):
    h, w = tile.shape
    grid = np.zeros((h * n, w * n), dtype=int)

    # iterate over all n*n tiles
    for x_i, y_i in product(range(n), repeat=2):
        # iterate over the values of the act tile
        for x, y in np.ndindex(tile.shape):
            v = (tile[x, y] - 1 + x_i + y_i) % 9 + 1
            grid[x + x_i * h, y + y_i * w] = v

    return grid


def load(data):
    return np.fromiter(data.replace("\n", ""), dtype=int).reshape(-1, data.index("\n"))


def main():
    puzzle = Puzzle(year=2021, day=15)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
