#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return [list(map(int, row.split())) for row in raw_data.strip().splitlines()]


def is_safe(row):
    diffs = [b - a for a, b in zip(row, row[1:])]
    decreasing = all(x < 0 for x in diffs)
    increasing = all(x > 0 for x in diffs)
    in_range = all(1 <= abs(x) <= 3 for x in diffs)
    return (decreasing or increasing) and in_range


@watch.measure_time
def solve1(data):
    return sum(is_safe(row) for row in data)


def try_is_safe(row):
    if is_safe(row):
        return True
    for i in range(len(row)):
        if is_safe([x for j, x in enumerate(row) if j != i]):
            return True
    return False


@watch.measure_time
def solve2(data):
    return sum(try_is_safe(row) for row in data)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
