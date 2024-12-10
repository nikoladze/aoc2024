#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return [[int(x) for x in row] for row in raw_data.strip().splitlines()]


def score(data, i, j, all=False):
    total = 0
    q = [(i, j)]
    visited = set()
    while q:
        i, j = q.pop()
        if not all:
            visited.add((i, j))
        if data[i][j] == 9:
            total += 1
            continue
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ii, jj = i + di, j + dj
            if not all and (ii, jj) in visited:
                continue
            if ii < 0 or jj < 0 or ii >= len(data) or jj >= len(data[0]):
                continue
            if (data[ii][jj] - data[i][j]) != 1:
                continue
            q.append((ii, jj))
    return total


@watch.measure_time
def solve1(data, all=False):
    zero_positions = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            if x == 0:
                zero_positions.append((i, j))
    return sum(score(data, *pos, all=all) for pos in zero_positions)


@watch.measure_time
def solve2(data):
    return solve1(data, all=True)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
