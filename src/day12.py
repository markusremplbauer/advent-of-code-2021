# Advent of Code 2021, Day 12
# markusremplbauer

import networkx as nx
from aocd.models import Puzzle
from funcy import ilen, print_calls

START, END = "start", "end"


@print_calls
def part1(graph):
    return ilen(dfs(graph, [START]))


@print_calls
def part2(graph):
    return ilen(dfs(graph, [START], double_visit=True))


def dfs(graph, path, double_visit=False):
    for n in graph.neighbors(path[-1]):
        if n == START:
            continue

        if (
            n.islower()
            and n in path
            and (
                not double_visit or any(path.count(e) > 1 and e.islower() for e in path)
            )
        ):
            continue

        new_path = path + [n]

        if n == END:
            yield new_path
            continue

        yield from dfs(graph, new_path, double_visit=double_visit)


def load(data):
    graph = nx.Graph()
    for line in data.splitlines():
        a, b = line.split("-")
        graph.add_edge(a, b)

    return graph


def main():
    puzzle = Puzzle(year=2021, day=12)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
