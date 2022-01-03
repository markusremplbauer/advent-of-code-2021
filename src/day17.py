# Advent of Code 2021, Day 17
# markusremplbauer

from itertools import count, repeat

import numpy as np
from aocd.models import Puzzle
from dotmap import DotMap
from funcy import concat, print_calls
from parse import parse


@print_calls
def part1(area):
    highpoint, _ = solve(area, min(area.y1, area.y2) - 1, max(area.x1, area.y2) + 1)
    return highpoint


@print_calls
def part2(area):
    _, velocities = solve(area, min(area.y1, area.y2) - 1, max(area.x1, area.x2) + 1)
    return len(velocities)


def solve(area, min_range, max_range):
    high = -np.inf
    velocities = set()

    for vx in range(max_range):
        for vy in range(min_range, max_range):
            peak = -np.inf
            for tx, ty in trajectory(vx, vy):
                peak = max(ty, peak)

                if in_area(tx, ty, area):
                    velocities.add((vx, vy))
                    high = max(high, peak)
                    break
                elif out_of_target(tx, ty, area):
                    break

    return high, velocities


def trajectory(vx, vy, x=0, y=0):
    avx = concat(range(vx, 0, -1 if vx > 0 else 1), repeat(0))
    avy = count(vy, -1)

    for dx, dy in zip(avx, avy):
        x += dx
        y += dy
        yield x, y


def in_area(x, y, area):
    return area.x1 <= x <= area.x2 and area.y1 <= y <= area.y2


def out_of_target(x, y, area):
    return x > area.x2 or y < area.y1


def load(data):
    return DotMap(parse("target area: x={x1:d}..{x2:d}, y={y1:d}..{y2:d}", data).named)


def main():
    puzzle = Puzzle(year=2021, day=17)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
