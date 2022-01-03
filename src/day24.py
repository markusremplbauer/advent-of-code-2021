# Advent of Code 2021, Day 24
# markusremplbauer

from itertools import product

from aocd.models import Puzzle
from funcy import collecting, print_calls

NUMBER_LENGTH = 14


@print_calls
def part1(instructions):
    facs = factors(instructions)
    # only the digits for cycle 1 must be permuted
    # the digits for cycle 2 can be calculated
    for digits in product(range(9, 0, -1), repeat=NUMBER_LENGTH // 2):
        model_numb = simulate(digits, facs)
        if model_numb:
            assert monad(facs, model_numb) == 0
            return "".join(map(str, model_numb))


@print_calls
def part2(instructions):
    facs = factors(instructions)
    for digits in product(range(1, 10), repeat=7):
        res = simulate(digits, facs)
        if res:
            assert monad(facs, res) == 0
            return "".join(map(str, res))


def simulate(digits, facs):
    z = 0
    model_numb = [0] * NUMBER_LENGTH

    digits_idx = 0

    for idx, (div_z, add_x, add_y) in enumerate(facs):
        # cycle 1: see rev_eng_cycle1()
        # z = 26 * z + w + add_y
        if add_x >= 0:
            w = digits[digits_idx]
            z = z * 26 + w + add_y
            model_numb[idx] = w
            digits_idx += 1

        # cycle 2: see rev_eng_cycle2()
        # z % 26 == w - add_x
        else:
            model_numb[idx] = (z % 26) + add_x
            z //= 26
            if not (1 <= model_numb[idx] <= 9):
                return False

    return model_numb


@collecting
def factors(instructions):
    for i in range(NUMBER_LENGTH):
        # only div_z, add_x, add_y effect z
        div_z = instructions[18 * i + 4][2]
        add_x = instructions[18 * i + 5][2]
        add_y = instructions[18 * i + 15][2]

        # cycle 1 or cycle 2
        assert (div_z == 1 and add_x >= 0) or (div_z == 26 and add_x < 0)

        yield div_z, add_x, add_y


def monad(facs, stdin):
    z = 0

    for (dz, ax, ay), w in zip(facs, stdin):
        # both reverse-engineered cycles should compute the same
        r1 = rev_eng_cycle1(dz, ax, ay, w, z)
        r2 = rev_eng_cycle2(ax, ay, w, z)
        assert r1 == r2

        z = r1

    return z


def rev_eng_cycle1(div_z, add_x, add_y, w, z):
    assert 1 <= w <= 9
    # [inp w | mul x 0 | add x z | mod x 26 | div z {DIVZ} | add x {ADDX}]
    x = (z % 26) + add_x
    z //= div_z
    # [eql x w | eql x 0]
    x = 1 if x != w else 0
    # [mul y 0 | add y 25 | mul y x | add y 1]
    y = (25 * x) + 1
    # [mul z y]
    z = z * y
    # [mul y 0 | add y w | add y {ADDY} | mul y x]
    y = (w + add_y) * x
    # [add z y]
    z = z + y
    # simplified: z = z * 26 + w + add_y
    return z


def rev_eng_cycle2(add_x, add_y, w, z):
    assert 1 <= w <= 9

    # inp w | mul x 0 | add x z | mod x 26
    x = z % 26
    #  div z {DIVZ}
    if add_x < 0:
        z //= 26

    # [add x {ADDX} | eql x w | eql x 0] if x == 0
    if x == w - add_x:
        return z

    # [add x {ADDX} | eql x w | eql x 0] if x == 1
    # [mul y 0 | add y 25 | mul y x | add y 1 | mul z y] -> z = z * 26
    # [mul y 0 | add y w | add y {ADDY} | mul y x | add z y] -> z = z + w + ay
    return 26 * z + w + add_y


@collecting
def load(data):
    for line in data.splitlines():
        parts = line.split(" ")

        if line.startswith("inp"):
            # one-argument instruction
            op, a, b = *parts, None

        else:
            # two-argument instruction
            op, a, b = parts

            try:
                b = int(b)
            except ValueError:
                pass

        yield op, a, b


def main():
    puzzle = Puzzle(year=2021, day=24)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
