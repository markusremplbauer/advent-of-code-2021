# Advent of Code 2021, Day 06
# markusremplbauer

from aocd.models import Puzzle
from funcy import lmap, print_calls


@print_calls
def part1(data):
    return solve(data=data, days=80)


@print_calls
def part2(data):
    return solve(data=data, days=256)


def solve(data, days):
    # there are 9 states a lanternfish can have
    states = [0] * 9
    for e in data:
        states[e] += 1

    for _ in range(days):
        # decreases is equivalent to a rolling to the left
        states[:-1], states[-1] = states[1:], states[0]

        # a 0 lanternfish timer is reset to 6
        states[6] += states[8]

    return sum(states)


def roll_left(arr, v):
    arr[v:], arr[:v] = arr[:v], arr[v:]


def load(data):
    return lmap(int, data.split(","))


def main():
    puzzle = Puzzle(year=2021, day=6)
    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
