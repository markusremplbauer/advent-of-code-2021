# Advent of Code 2021, Day 02
# markusremplbauer

from aocd.models import Puzzle
from funcy import print_calls


@print_calls
def part1(instructions):
    hor, dep = 0, 0
    for instruction in instructions:
        d, v = instruction[0], int(instruction[1])
        if d == "up":
            dep -= v
        elif d == "down":
            dep += v
        elif d == "forward":
            hor += v
    return hor * dep


@print_calls
def part2(instructions):
    hor, dep, aim = 0, 0, 0
    for instruction in instructions:
        dir, val = instruction[0], int(instruction[1])
        if dir == "up":
            aim -= val
        elif dir == "down":
            aim += val
        elif dir == "forward":
            hor += val
            dep += aim * val
    return hor * dep


def load(data):
    return [line.split(" ") for line in data.split("\n")]


def main():
    puzzle = Puzzle(year=2021, day=2)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
