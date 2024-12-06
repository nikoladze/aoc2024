#!/usr/bin/env python

from functools import partial
from itertools import cycle
from pathlib import Path

from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def get_start(data):
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            if x not in "#.":
                return (i, j)


@watch.measure_time
def solve1(data):
    nrows = len(data)
    ncols = len(data[0])
    directions = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
    i, j = get_start(data)
    di, dj = next(directions)
    visited = set()
    while i >= 0 and j >= 0 and i < nrows and j < ncols:
        if data[i][j] == "#":
            i, j = i - di, j - dj  # go back
            di, dj = next(directions)
        else:
            visited.add((i, j))
        i, j = i + di, j + dj
    return len(visited)


def is_loop(data, i, j, obstacle):
    nrows = len(data)
    ncols = len(data[0])
    directions = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
    di, dj = next(directions)
    visited = set()
    while i >= 0 and j >= 0 and i < nrows and j < ncols:
        if data[i][j] == "#" or (i, j) == obstacle:
            i, j = i - di, j - dj  # go back
            di, dj = next(directions)
        else:
            visited.add((i, j, di, dj))
        i, j = i + di, j + dj
        if (i, j, di, dj) in visited:
            return True
    return False


@watch.measure_time
def solve2(data):
    obstacles = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            if x == ".":
                obstacles.append((i, j))
    i, j = get_start(data)
    return sum(map(partial(is_loop, data, i, j), obstacles))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
