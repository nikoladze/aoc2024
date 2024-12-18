#!/usr/bin/env python

import heapq
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return [tuple(map(int, line.split(","))) for line in raw_data.strip().splitlines()]


def solve(data, maxx=70, maxy=70):
    corrupted = set(data)
    q = [(0, 0, 0)]
    best_scores = {}
    while q:
        score, x, y = heapq.heappop(q)
        if (x, y) in best_scores and best_scores[x, y] <= score:
            continue
        best_scores[x, y] = score
        if x == maxx and y == maxy:
            return score
        for x, y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if x < 0 or y < 0 or x > maxx or y > maxy:
                continue
            if (x, y) in corrupted:
                continue
            heapq.heappush(q, (score + 1, x, y))


@watch.measure_time
def solve1(data):
    return solve(data[:1024])


@watch.measure_time
def solve2(data):
    for i, byte in enumerate(data[1024:], 1024):
        print(i, end="\r")
        if solve(data[: i + 1]) is None:
            return ",".join(map(str, byte))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
