# Advent of Code 2021, Day 20
# markusremplbauer

from collections import defaultdict

from aocd.models import Puzzle
from funcy import first, lmap, print_calls, second


@print_calls
def part1(img, lookup):
    return solve(img, lookup, 2)


@print_calls
def part2(img, lookup):
    return solve(img, lookup, 50)


def solve(img, lookup, steps):
    void = "0"
    for _ in range(steps):
        img, void = enhance(img, lookup, void)

    return list(img.values()).count("1")


def enhance(img, lookup, void):
    img.default_factory = lambda: void
    res = defaultdict(lambda: void)

    xs, ys = lmap(first, img.keys()), lmap(second, img.keys())
    x_min, x_max, y_min, y_max = min(xs), max(xs), min(ys), max(ys)

    # iterate over pixels with a padding of 1
    for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
            idx = int(bits(img, x, y), 2)
            res[(x, y)] = lookup[idx]

    # get the output pixel of void pixels
    new_void = lookup[int(void * 9, 2)]
    return res, new_void


def bits(img, x, y):
    return "".join(img[adj] for adj in adjacent(x, y))


def adjacent(x, y):
    return (
        # row 1
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        # row 2
        (x - 1, y),
        (x, y),
        (x + 1, y),
        # row 2
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    )


def load(data):
    data = data.replace("#", "1").replace(".", "0")
    blocks = data.split("\n\n")

    # image enhancement algorithm string
    lookup = blocks[0]
    img = defaultdict()
    for y, line in enumerate(blocks[1].splitlines()):
        for x, px in enumerate(line):
            img[(x, y)] = px

    return img, lookup


def main():
    puzzle = Puzzle(year=2021, day=20)

    ans1 = part1(*load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(*load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
