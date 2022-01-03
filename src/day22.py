# Advent of Code 2021, Day 22
# markusremplbauer

import numpy as np
from aocd.models import Puzzle
from dotmap import DotMap
from funcy import print_calls
from parse import parse


@print_calls
def part1(steps):
    grid = np.zeros((101, 101, 101), dtype=bool)
    for step in steps:
        x1, x2 = max(step.x1, -50), min(step.x2, 50)
        y1, y2 = max(step.y1, -50), min(step.y2, 50)
        z1, z2 = max(step.z1, -50), min(step.z2, 50)

        index = np.ix_(range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1))
        grid[index] = step.state == "on"

    return grid.sum()


@print_calls
def part2(steps):
    cubeset = CubeSet()

    for step in steps:
        # the CubeSet assumes that endpoints are inclusive
        cubeset.assign(
            Cube(step.x1, step.x2 + 1, step.y1, step.y2 + 1, step.z1, step.z2 + 1),
            step.state,
        )

    return cubeset.volume()


class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.z1, self.z2 = z1, z2


class CubeSet:
    def __init__(self):
        self.cubes: set[Cube] = set()

    def assign(self, cube: Cube, state: str):
        # make room for the new cube by clearing that space
        overlapping = {c for c in self.cubes if CubeSet.overlap(c, cube)}
        for overlap in overlapping:
            self.subtract(overlap, cube)

        # should the cube be on
        if state == "on":
            self.cubes.add(cube)

    @staticmethod
    def overlap(a: Cube, b: Cube):
        # checks if two cubes a and b overlap
        x = a.x1 < b.x2 and b.x1 < a.x2
        y = a.y1 < b.y2 and b.y1 < a.y2
        z = a.z1 < b.z2 and b.z1 < a.z2

        return x and y and z

    def subtract(self, a: Cube, b: Cube):
        # we split a to make space for b
        self.cubes.remove(a)

        # splits of a and the remaining split overlapping with b
        s1, s2, remaining = None, None, None

        xl, xr = a.x1 < b.x1, a.x2 > b.x2
        yl, yr = a.y1 < b.y1, a.y2 > b.y2
        zl, zr = a.z1 < b.z1, a.z2 > b.z2

        # split in x possible?
        if xl or xr:
            mx = b.x1 if xl else b.x2
            s1 = Cube(a.x1, mx, a.y1, a.y2, a.z1, a.z2)
            s2 = Cube(mx, a.x2, a.y1, a.y2, a.z1, a.z2)
            remaining = s2 if xl else s1

        # split in y possible?
        elif yl or yr:
            my = b.y1 if yl else b.y2
            s1 = Cube(a.x1, a.x2, a.y1, my, a.z1, a.z2)
            s2 = Cube(a.x1, a.x2, my, a.y2, a.z1, a.z2)
            remaining = s2 if yl else s1

        # split in z possible?
        elif zl or zr:
            mz = b.z1 if zl else b.z2
            s1 = Cube(a.x1, a.x2, a.y1, a.y2, a.z1, mz)
            s2 = Cube(a.x1, a.x2, a.y1, a.y2, mz, a.z2)
            remaining = s2 if zl else s1

        # nothing to split?
        else:
            return

        # add the two new cubes
        self.cubes.add(s1)
        self.cubes.add(s2)

        # continue splitting the remaining overlapping cube
        self.subtract(remaining, b)

    def volume(self):
        return sum(
            (cube.x2 - cube.x1) * (cube.y2 - cube.y1) * (cube.z2 - cube.z1)
            for cube in self.cubes
        )


def load(data):
    return [
        DotMap(
            parse(
                "{state:w} x={x1:d}..{x2:d},y={y1:d}..{y2:d},z={z1:d}..{z2:d}",
                line,
            ).named
        )
        for line in data.splitlines()
    ]


def main():
    puzzle = Puzzle(year=2021, day=22)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
