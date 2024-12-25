#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    blocks = raw_data.strip().split("\n\n")
    return [block.splitlines() for block in blocks]


def is_overlapping(key, lock):
    for i, row in enumerate(lock):
        for j, c in enumerate(row):
            if c == "#" and key[i][j] == "#":
                return True
    return False


@watch.measure_time
def solve1(data):
    locks = []
    keys = []
    for block in data:
        if all(c == "#" for c in block[-1]):
            keys.append(block)
        else:
            locks.append(block)
    total = 0
    for key in keys:
        for lock in locks:
            if is_overlapping(key, lock):
                continue
            total += 1
    return total


@watch.measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
