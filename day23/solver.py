#!/usr/bin/env python

from itertools import combinations
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return [line.split("-") for line in raw_data.strip().splitlines()]


@watch.measure_time
def solve1(data):
    graph = {}
    for a, b in data:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    checked = set()
    groups = []
    total = 0
    for a, bs in graph.items():
        for c, d in combinations(bs, 2):
            if frozenset([a, c, d]) in checked:
                continue
            if d in graph[c]:
                groups.append((a, c, d))
            checked.add(frozenset([a, c, d]))
    return sum(any(x.startswith("t") for x in [a, b, c]) for a, b, c in groups)


@watch.measure_time
def solve2(data):
    graph = {}
    for a, b in data:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    def is_connected(group):
        for a, b in combinations(group, 2):
            if b not in graph[a]:
                return False
        return True

    checked = set()
    groups = []
    total = 0
    for a, bs in graph.items():
        for k in range(2, len(bs) + 1):
            for group in combinations(bs, k):
                key = frozenset(group) | {a}
                if key in checked:
                    continue
                if is_connected(group):
                    groups.append(key)
                checked.add(key)
    largest = max((group for group in groups), key=lambda group: len(group))
    return ",".join(sorted(largest))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
