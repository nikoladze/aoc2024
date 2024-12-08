#!/usr/bin/env python

from itertools import combinations
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


@watch.measure_time
def solve1(data):
    antennas = {}
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == ".":
                continue
            antennas.setdefault(c, []).append((i, j))
    unique_anti_in_grid = set()
    for positions in antennas.values():
        for a, b in combinations(positions, 2):
            di = b[0] - a[0]
            dj = b[1] - a[1]
            anti1 = (a[0] - di, a[1] - dj)
            anti2 = (b[0] + di, b[1] + dj)
            for anti in [anti1, anti2]:
                i, j = anti
                if i >= 0 and j >= 0 and i < len(data) and j < len(data[0]):
                    unique_anti_in_grid.add(anti)
    return len(unique_anti_in_grid)


@watch.measure_time
def solve2(data):
    antennas = {}
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == ".":
                continue
            antennas.setdefault(c, []).append((i, j))
    unique_anti_in_grid = set()
    for positions in antennas.values():
        for a, b in combinations(positions, 2):
            di = b[0] - a[0]
            dj = b[1] - a[1]
            for start in [a, b]:
                for sign in [-1, 1]:
                    i, j = start
                    while i >= 0 and j >= 0 and i < len(data) and j < len(data[0]):
                        unique_anti_in_grid.add((i, j))
                        i, j = i + sign * di, j + sign * dj
    return len(unique_anti_in_grid)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
