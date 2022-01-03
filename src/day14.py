# Advent of Code 2021, Day 14
# markusremplbauer

from collections import Counter

from aocd.models import Puzzle
from funcy import print_calls
from parse import parse


@print_calls
def part1(polymer, rules):
    return solve(polymer, rules, steps=10)


@print_calls
def part2(polymer, rules):
    return solve(polymer, rules)


def solve(polymer, rules: dict, steps=40):
    counts = Counter()

    # all initial pairs
    for a, b in zip(polymer[:-1], polymer[1:]):
        counts[a + b] += 1

    for _ in range(steps):
        step = counts.copy()
        for key, count in counts.items():
            if key in rules:
                a, b = rules[key]

                # the original pair is replaced by two new ones
                # (AB -> C) -> AC and BC
                step[key] -= count
                step[a] += count
                step[b] += count

        counts = step

    letters = Counter()
    for key, count in counts.items():
        letters[key[0]] += count

    # last letter has no pair
    letters[polymer[-1]] += 1

    most = letters.most_common(1)[0][1]
    least = letters.most_common()[-1][1]

    return most - least


def load(data):
    polymer, in_rules = data.split("\n\n")
    rules = {}
    for line in in_rules.splitlines():
        a, b, v = parse("{:l}{:l} -> {:l}", line)
        rules[a + b] = (a + v, v + b)

    return polymer, rules


def main():
    puzzle = Puzzle(year=2021, day=14)

    ans1 = part1(*load(puzzle.input_data))
    # puzzle.answer_a = ans1

    ans2 = part2(*load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
