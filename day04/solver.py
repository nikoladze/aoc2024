#!/usr/bin/env python

from itertools import chain
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    table = raw_data.strip().splitlines()
    return [[(i, j, x) for j, x in enumerate(row)] for i, row in enumerate(table)]


def rolling(x, n=4):
    x = list(x)
    for i in range(len(x) - n + 1):
        yield x[i : i + n]


def iterate(data, i, j, di, dj):
    ncols = len(data[0])
    nrows = len(data)
    while True:
        if i < 0 or j < 0 or i >= nrows or j >= ncols:
            return
        yield data[i][j]
        i += di
        j += dj


def horizontal(data):
    for row in data:
        yield row


def vertical(data):
    for icol in range(len(data[0])):
        yield [row[icol] for row in data]


def diagonal(data):
    ncols = len(data[0])
    nrows = len(data)
    for icol in range(ncols):
        yield iterate(data, 0, icol, 1, 1)
        yield iterate(data, nrows - 1, icol, -1, 1)
    for irow in range(1, nrows):
        yield iterate(data, irow, 0, 1, 1)
    for irow in range(nrows - 1):
        yield iterate(data, irow, 0, -1, 1)


@watch.measure_time
def solve1(data):
    debug = [["." for __ in range(len(data[0]))] for __ in range(len(data))]
    total = 0
    for sub in chain(
        horizontal(data),
        vertical(data),
        diagonal(data),
    ):
        for candidate in rolling(sub):
            c = "".join(x[2] for x in candidate)
            if c == "XMAS" or c[::-1] == "XMAS":
                for i, j, x in candidate:
                    debug[i][j] = x
                total += 1
    print()
    print("\n".join("".join(row) for row in debug))
    print()
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
            if is_xmas([[x[2] for x in row[j : j + 3]] for row in data[i : i + 3]]):
                total += 1
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
