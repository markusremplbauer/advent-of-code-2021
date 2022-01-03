# Advent of Code 2021, Day 13
# markusremplbauer

import matplotlib.pylab as plt
import numpy as np
from aocd.models import Puzzle
from funcy import print_calls
from parse import parse


@print_calls
def part1(dots, folds):
    return solve(dots, folds, first_fold=True)


@print_calls
def part2(dots, folds):
    return solve(dots, folds)


def solve(dots, folds, first_fold=False):
    paper = fill_paper(dots)
    for d, v in folds:
        fold = fold_x if d == "x" else fold_y
        paper = fold(paper, v)

        if first_fold:
            break

    paper[paper >= 1] = 1
    plt.imshow(paper)
    plt.show()
    return paper.sum()


def fold_x(paper, x):
    right = paper[:, (x + 1) :]
    right = np.fliplr(right)

    left = paper[:, :x]
    paper = left + right

    return paper


def fold_y(paper, y):
    lower = paper[(y + 1) :, :]
    lower = np.flipud(lower)

    upper = paper[:y, :]
    paper = upper + lower

    return paper


def fill_paper(dots):
    width, height = dots.max(axis=0) + 1

    paper = np.zeros((height, width), dtype=int)
    for x, y in dots:
        paper[y, x] = 1

    return paper


def load(data):
    in_dots, in_folds = data.split("\n\n")
    dots = [tuple(parse("{:d},{:d}", line)) for line in in_dots.split("\n")]
    dots = np.array(dots)

    folds = [
        tuple(parse("fold along {:w}={:d}", line)) for line in in_folds.split("\n")
    ]

    return dots, folds


def main():
    puzzle = Puzzle(year=2021, day=13)

    ans1 = part1(*load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(*load(puzzle.input_data))
    # answer to part 2 are the eight plotted capital letters
    # puzzle.answer_b = "PZEHRAER"


if __name__ == "__main__":
    main()
