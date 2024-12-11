#!/usr/bin/env python

from functools import cache
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return list(map(int, raw_data.strip().split()))


@cache
def expand(stone, n):
    if n == 0:
        return 1
    elif stone == 0:
        return expand(1, n - 1)
    elif len(str(stone)) % 2 == 0:
        i = len(str(stone)) // 2
        left = expand(int(str(stone)[:i]), n - 1)
        right = expand(int(str(stone)[i:]), n - 1)
        return left + right
    else:
        return expand(stone * 2024, n - 1)


@watch.measure_time
def solve1(data):
    return sum(expand(x, n=25) for x in data)


@watch.measure_time
def solve2(data):
    return sum(expand(x, n=75) for x in data)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
