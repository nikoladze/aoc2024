#!/usr/bin/env python

from pathlib import Path
from collections import Counter
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    lefts, rights = zip(*(map(int, line.split()) for line in raw_data.splitlines()))
    return lefts, rights


@watch.measure_time
def solve1(data):
    lefts, rights = data
    return sum(abs(right - left) for left, right in zip(sorted(lefts), sorted(rights)))


@watch.measure_time
def solve2(data):
    lefts, rights = data
    counts = Counter(rights)
    return sum(counts.get(left, 0) * left for left in lefts)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
