# Advent of Code 2021, Day 23
# markusremplbauer

from copy import deepcopy

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls
from parse import parse

# amount of energy an amphipod requires to move a step
ENERGY = {"A": 1, "B": 10, "C": 100, "D": 1000}

DP = {}


@print_calls
def part1(hallway, rooms):
    return solve(hallway, rooms)


@print_calls
def part2(hallway, rooms):
    return solve(hallway, rooms)


def solve(hallway, rooms):
    key = (tuple(hallway), tuple((k, tuple(room)) for k, room in rooms.items()))

    if done(rooms):
        return 0

    if key in DP:
        return DP[key]

    # move to dest if possible
    for idx, e in enumerate(hallway):
        if e in rooms and can_move_to(e, rooms[e]) and clear_path(e, idx, hallway):
            return move_to_room(hallway, rooms, e, idx)

    ans = np.inf
    for k, room in rooms.items():
        if not can_move_from(k, room):
            continue

        h_idx = hallway_idx(room)
        if h_idx is None:
            continue

        e = room[h_idx]
        for to_idx in range(len(hallway)):
            if to_idx in [2, 4, 6, 8] or hallway[to_idx] != "E":
                continue

            if clear_path(k, to_idx, hallway):
                # move to dest
                dist = h_idx + 1 + abs(to_idx - amphipod_idx(k))

                new_hallway = list(hallway)
                new_hallway[to_idx] = e

                new_rooms = deepcopy(rooms)
                new_rooms[k][h_idx] = "E"

                ans = min(ans, ENERGY[e] * dist + solve(new_hallway, new_rooms))

    DP[key] = ans
    return ans


def done(rooms):
    for k, v in rooms.items():
        for e in v:
            if e != k:
                return False
    return True


def move_to_room(hallway, rooms, e, idx):
    d_idx = dest_idx(rooms[e])
    dist = d_idx + 1 + abs(amphipod_idx(e) - idx)
    cost = ENERGY[e] * dist

    new_hallway = list(hallway)
    new_hallway[idx] = "E"

    new_rooms = deepcopy(rooms)
    new_rooms[e][d_idx] = e

    return cost + solve(new_hallway, new_rooms)


def can_move_from(amphipod, room):
    return any(p not in [amphipod, "E"] for p in room)


def can_move_to(amphipod, room):
    return all(p in [amphipod, "E"] for p in room)


def clear_path(amphipod, hallway_idx, hallway):
    return not any(
        between(idx, amphipod_idx(amphipod), hallway_idx) and hallway[idx] != "E"
        for idx in range(len(hallway))
    )


def between(idx, amphipod_idx, hallway_idx):
    return (amphipod_idx < idx < hallway_idx) or (hallway_idx < idx < amphipod_idx)


def amphipod_idx(amphipod):
    return {"A": 2, "B": 4, "C": 6, "D": 8}[amphipod]


def dest_idx(room):
    for i, c in reversed(list(enumerate(room))):
        if c == "E":
            return i
    return None


def hallway_idx(room):
    for i, e in enumerate(room):
        if e != "E":
            return i
    return None


def load(data, part=1):
    lines = data.splitlines()

    hallway = ["E"] * (len(lines[1]) - 2)
    rooms_top = parse("###{:w}#{:w}#{:w}#{:w}###", lines[2])
    rooms_bot = parse("  #{:w}#{:w}#{:w}#{:w}#", lines[3])
    if part == 2:
        v1 = parse("  #{:w}#{:w}#{:w}#{:w}#", "  #D#C#B#A#")
        v2 = parse("  #{:w}#{:w}#{:w}#{:w}#", "  #D#B#A#C#")
        rooms = {
            "A": [rooms_top[0], v1[0], v2[0], rooms_bot[0]],
            "B": [rooms_top[1], v1[1], v2[1], rooms_bot[1]],
            "C": [rooms_top[2], v1[2], v2[2], rooms_bot[2]],
            "D": [rooms_top[3], v1[3], v2[3], rooms_bot[3]],
        }
    else:
        rooms = {
            "A": [rooms_top[0], rooms_bot[0]],
            "B": [rooms_top[1], rooms_bot[1]],
            "C": [rooms_top[2], rooms_bot[2]],
            "D": [rooms_top[3], rooms_bot[3]],
        }

    return hallway, rooms


def main():
    puzzle = Puzzle(year=2021, day=23)

    ans1 = part1(*load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(*load(puzzle.input_data, part=2))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
