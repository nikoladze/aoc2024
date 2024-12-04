#!/usr/bin/env python

from itertools import chain
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def horizontals(data):
    for row in data:
        yield row


def verticals(data):
    for icol in range(len(data[0])):
        yield [row[icol] for row in data]


def iterate(data, i, j, di, dj):
    ncols = len(data[0])
    nrows = len(data)
    while True:
        if i < 0 or j < 0 or i >= nrows or j >= ncols:
            return
        yield data[i][j]
        i, j = i + di, j + dj


def diagonals(data):
    ncols = len(data[0])
    nrows = len(data)
    for icol in range(ncols):
        yield iterate(data, 0, icol, 1, 1)
        yield iterate(data, nrows - 1, icol, -1, 1)
    for irow in range(1, nrows):
        yield iterate(data, irow, 0, 1, 1)
    for irow in range(nrows - 1):
        yield iterate(data, irow, 0, -1, 1)


def rolling(x, n=4):
    x = list(x)
    for i in range(len(x) - n + 1):
        yield "".join(x[i : i + n])


@watch.measure_time
def solve1(data):
    total = 0
    for sub in chain(
        horizontals(data),
        verticals(data),
        diagonals(data),
    ):
        for candidate in rolling(sub):
            if candidate in ["XMAS", "SAMX"]:
                total += 1
    return total


def is_mas(s):
    s = "".join(s)
    if s in ["MAS", "SAM"]:
        return True
    else:
        return False


def is_xmas(x):
    return is_mas([x[0][0], x[1][1], x[2][2]]) and is_mas([x[2][0], x[1][1], x[0][2]])


@watch.measure_time
def solve2(data):
    total = 0
    ncols = len(data[0])
    nrows = len(data)
    for i in range(nrows - 3 + 1):
        for j in range(ncols - 3 + 1):
            if is_xmas([row[j : j + 3] for row in data[i : i + 3]]):
                total += 1
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
