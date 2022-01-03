# Advent of Code 2021, Day 18
# markusremplbauer

from copy import deepcopy
from functools import reduce
from math import ceil, floor
from operator import add

from anytree import NodeMixin, PreOrderIter, RenderTree
from aocd.models import Puzzle
from funcy import lmap, print_calls, with_next, with_prev
from tqdm.auto import tqdm


@print_calls
def part1(snails):
    res = reduce(add, snails)
    return res.get_magnitude()


@print_calls
def part2(snails):
    max_magnitude = 0
    for i in tqdm(range(len(snails))):
        for j in range(len(snails)):
            # perform deep copy because of my mutable tree transforms
            max_magnitude = max(
                (deepcopy(snails[i]) + deepcopy(snails[j])).get_magnitude(),
                max_magnitude,
            )

    return max_magnitude


class SnailNode(NodeMixin):
    def __init__(self, val=None, parent=None, children=None):
        self.val = val
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        if not self.children:
            return str(self.val)
        return "[" + ",".join(map(repr, self.children)) + "]"

    def __add__(self, other):
        root = SnailNode(children=[self, other])
        root.reduce()
        return root

    def reduce(self):
        while True:
            match = False

            for node in PreOrderIter(self, filter_=lambda n: n.is_leaf_pair()):
                if node.depth == 4:
                    node.explode()
                    match = True
                    break

            if match:
                continue

            for node in PreOrderIter(self, filter_=lambda n: n.is_leaf):
                if node.val >= 10:
                    node.split()
                    match = True
                    break

            if not match:
                break

    def explode(self):
        left, right = self.children
        closest_left, closest_right = left.closest_left(), right.closest_right()

        if closest_left:
            closest_left.val += left.val
        if closest_right:
            closest_right.val += right.val

        self.children = []
        self.val = 0

    def split(self):
        left, right = SnailNode(floor(self.val / 2)), SnailNode(ceil(self.val / 2))
        self.children = [left, right]
        self.val = None

    def closest_left(self):
        return self.closest_sibling(with_prev)

    def closest_right(self):
        return self.closest_sibling(with_next)

    def closest_sibling(self, window):
        order = PreOrderIter(self.root, filter_=lambda n: n.is_leaf)
        for node, other in window(order):
            if node == self:
                return other

    def is_leaf_pair(self):
        if not self.children:
            return False

        left, right = self.children
        return left.is_leaf and right.is_leaf

    def get_magnitude(self):
        if self.is_leaf:
            return self.val

        left, right = self.children
        return 3 * left.get_magnitude() + 2 * right.get_magnitude()

    def render(self):
        print(RenderTree(self))


def load(data):
    return lmap(load_line, data.splitlines())


def load_line(line):
    val = eval(line)

    def _transform(val):
        if isinstance(val, list):
            return SnailNode(children=[_transform(val[0]), _transform(val[1])])
        else:
            return SnailNode(val)

    return _transform(val)


def main():
    puzzle = Puzzle(year=2021, day=18)

    ans1 = part1(load(puzzle.input_data))
    # puzzle.answer_a = ans1
    ans2 = part2(load(puzzle.input_data))
    # puzzle.answer_b = ans2


if __name__ == "__main__":
    main()
