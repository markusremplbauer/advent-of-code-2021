# Advent of Code 2021, Day 03
# markusremplbauer
import numpy as np
from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(data):
    gamma, epsilon = "", ""
    for col in data.T:
        bins = np.bincount(col)
        gamma += str(np.argmax(bins))
        epsilon += str(np.argmin(bins))

    # power consumption
    return int(gamma, 2) * int(epsilon, 2)


@print_calls
def part2(data):
    v_ogr = data
    v_sr = data
    for i, col in enumerate(data.T):
        bins_ogr = np.bincount(v_ogr.T[i])
        bins_sr = np.bincount(v_sr.T[i])

        # filter oxygen generator rating
        if v_ogr.shape[0] > 1:
            if bins_ogr[0] == bins_ogr[1]:
                v_ogr = v_ogr[v_ogr[:, i] == 1]
            else:
                v_ogr = v_ogr[v_ogr[:, i] == np.argmax(bins_ogr)]

        # filter CO2 scrubber rating
        if v_sr.shape[0] > 1:
            if bins_sr[0] == bins_sr[1]:
                v_sr = v_sr[v_sr[:, i] == 0]
            else:
                v_sr = v_sr[v_sr[:, i] == np.argmin(bins_sr)]

    ogr = int("".join(str(e) for e in v_ogr[0]), 2)
    sr = int("".join(str(e) for e in v_sr[0]), 2)

    return ogr * sr


def load(data):
    return np.fromiter(data.replace("\n", ""), dtype=int).reshape(-1, data.index("\n"))


def main():
    puzzle = Puzzle(year=2021, day=3)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
