#!/usr/bin/env python

from functools import cmp_to_key
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    blocks = raw_data.strip().split("\n\n")
    gt = {}
    for line in blocks[0].splitlines():
        a, b = map(int, line.split("|"))
        gt[b, a] = True
        gt[a, b] = False
    updates = [tuple(map(int, line.split(","))) for line in blocks[1].splitlines()]
    return gt, updates


def is_sorted(line, gt):
    for a, b in zip(line, line[1:]):
        if not gt[b, a]:
            return False
    return True


@watch.measure_time
def solve1(data):
    total = 0
    gt, updates = data
    for line in updates:
        if is_sorted(line, gt):
            total += line[len(line) // 2]
    return total


@watch.measure_time
def solve2(data):
    total = 0
    gt, updates = data
    for line in updates:
        if not is_sorted(line, gt):
            sorted_line = sorted(
                line, key=cmp_to_key(lambda a, b: 1 if gt[a, b] else -1)
            )
            total += sorted_line[len(line) // 2]
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
