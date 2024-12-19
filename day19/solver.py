#!/usr/bin/env python

from functools import cache
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    towels, patterns = raw_data.strip().split("\n\n")
    return set(towels.split(", ")), patterns.splitlines()


@watch.measure_time
def solve1(data):
    towels, patterns = data
    maxlen = max(len(towel) for towel in towels)

    @cache
    def is_valid(pattern):
        if pattern in towels:
            return True
        for i in range(min(maxlen, len(pattern)), 0, -1):
            if pattern[:i] in towels and is_valid(pattern[i:]):
                return True
        return False

    return sum(map(is_valid, patterns))


@watch.measure_time
def solve2(data):
    towels, patterns = data
    maxlen = max(len(towel) for towel in towels)

    @cache
    def count_valid(pattern):
        if len(pattern) == 0:
            return 1
        return sum(
            count_valid(pattern[i:])
            for i in range(min(maxlen, len(pattern)), 0, -1)
            if pattern[:i] in towels
        )

    return sum(map(count_valid, patterns))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
