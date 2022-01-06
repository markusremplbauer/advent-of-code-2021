# Advent of Code 2021, Day 16
# markusremplbauer

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls

version_sum = 0


@print_calls
def part1(data):
    solve(data)

    global version_sum
    return version_sum


@print_calls
def part2(data):
    return solve(data)


def solve(data):
    idx = 0
    value, _ = get_pkg_value(data, idx)
    return value


def get_pkg_value(data, idx):
    version, type_id, idx = parse_pkg_header(data, idx)
    if type_id == 4:
        value, idx = parse_literal_pkg(data, idx)
    else:
        value, idx = parse_operator_pkg(data, idx, type_id)
    return value, idx


def parse_pkg_header(data, idx):
    version = int(data[idx : idx + 3], 2)
    global version_sum
    version_sum += version

    type_id = int(data[idx + 3 : idx + 6], 2)
    idx += 6

    return version, type_id, idx


def parse_literal_pkg(data, idx):
    literal = ""
    while data[idx] != "0":
        literal += data[idx + 1 : idx + 5]
        idx += 5

    literal += data[idx + 1 : idx + 5]
    idx += 5
    return int(literal, 2), idx


def parse_operator_pkg(data, idx, p_type_id):
    type_id = int(data[idx])
    idx += 1
    literals = []
    if type_id == 0:
        l_s_p = int(data[idx : idx + 15], 2)
        idx += 15
        start_idx = idx
        while idx < start_idx + l_s_p:
            literal, idx = get_pkg_value(data, idx)
            literals.append(literal)
    elif type_id == 1:
        c_s_p = int(data[idx : idx + 11], 2)
        idx += 11
        for _ in range(c_s_p):
            literal, idx = get_pkg_value(data, idx)
            literals.append(literal)

    return perform_operation(p_type_id, literals), idx


def perform_operation(type_id, literals):
    if type_id == 0:
        return sum(literals)
    elif type_id == 1:
        return np.prod(literals)
    elif type_id == 2:
        return min(literals)
    elif type_id == 3:
        return max(literals)
    elif type_id == 5:
        return 1 if literals[0] > literals[1] else 0
    elif type_id == 6:
        return 1 if literals[0] < literals[1] else 0
    elif type_id == 7:
        return 1 if literals[0] == literals[1] else 0


def load(data):
    bin_length = len(data) * 4
    return bin(int(data, 16))[2:].zfill(bin_length)


def main():
    puzzle = Puzzle(year=2021, day=16)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
