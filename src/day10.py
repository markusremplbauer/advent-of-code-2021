# Advent of Code 2021, Day 10
# markusremplbauer

from aocd.models import Puzzle
from funcy import print_calls

opening = ["(", "[", "{", "<"]
closing = [")", "]", "}", ">"]
mappings = {
    ")": {"opening": "(", "illegal": 3, "incomplete": 1},
    "]": {"opening": "[", "illegal": 57, "incomplete": 2},
    "}": {"opening": "{", "illegal": 1197, "incomplete": 3},
    ">": {"opening": "<", "illegal": 25137, "incomplete": 4},
}


def parse_line(line):
    values = []
    for e in line:
        if e in opening:
            values.append(e)
        elif e in closing and mappings[e]["opening"] == values[-1]:
            values.pop()
        else:
            return mappings[e]["illegal"], None

    comp = "".join(
        reversed([k for e in values for k, v in mappings.items() if v["opening"] == e])
    )
    return 0, comp


@print_calls
def part1(data):
    err = 0
    for line in data:
        e_res, _ = parse_line(line)
        err += e_res

    return err


@print_calls
def part2(data):
    scores = []
    for line in data:
        _, comp = parse_line(line)

        if comp is not None:
            score = 0
            for e in comp:
                score *= 5
                score += mappings[e]["incomplete"]

            scores.append(score)

    return sorted(scores)[len(scores) // 2]


def load(data):
    return data.splitlines()


def main():
    puzzle = Puzzle(year=2021, day=10)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
