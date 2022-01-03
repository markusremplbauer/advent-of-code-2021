# Advent of Code 2021, Day 08
# markusremplbauer

from collections import namedtuple

from aocd.models import Puzzle
from funcy import collecting, first, lcat, lmap, lwithout, print_calls

Chunk = namedtuple("Chunk", "wires display")


@print_calls
def part1(chunks):
    return sum(
        # count the digits 1, 4, 7, 8 identified by their segment count
        sum(len(ch) in (2, 3, 4, 7) for ch in chunk.display)
        for chunk in chunks
    )


@print_calls
def part2(chunks):
    res = 0
    for chunk in chunks:
        code = decode(chunk)

        # decode digit by digit and sum up the result
        num = "".join(map(str, (code[digit] for digit in chunk.display)))
        res += int(num)

    return res


def decode(chunk):
    wires = chunk.wires
    code = {
        1: first(w for w in wires if len(w) == 2),
        4: first(w for w in wires if len(w) == 4),
        7: first(w for w in wires if len(w) == 3),
        8: first(w for w in wires if len(w) == 7),
    }
    wires = lwithout(wires, *code.values())

    # the remaining digits have segment a and g in common
    ag = set.intersection(*wires)

    # logical identify segments
    a = code[7] - code[1]
    eg = code[8] - (code[4] | a)
    bd = code[8] - code[7] - eg
    g = ag - a
    e = eg - g

    # destruct digit 9
    code[9] = code[8] - e
    wires = lwithout(wires, code[9])

    # 0 misses segment d and 6 segment c
    dc = set(lcat(e for e in (code[8] - w for w in wires) if len(e) == 1))

    # logical identify the remaining segments
    d = set.intersection(dc, bd)
    c = dc - d
    b = bd - d
    f = code[1] - c

    # destruct digits 0, 2, 3, 5, 6
    code[0] = code[8] - d
    code[2] = code[8] - b - f
    code[3] = code[7] | d | g
    code[5] = code[8] - c - e
    code[6] = code[8] - c

    return {frozenset(v): k for k, v in code.items()}


@collecting
def load(data):
    chunks = [line.split(" | ") for line in data.split("\n")]
    for chunk in chunks:
        wires = lmap(set, chunk[0].split())
        display = lmap(frozenset, chunk[1].split())
        yield Chunk(wires, display)


def main():
    puzzle = Puzzle(year=2021, day=8)
    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
