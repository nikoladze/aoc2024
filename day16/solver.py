#!/usr/bin/env python

from heapq import heappush, heappop
from collections import deque
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def iter_paths(data):
    nrows = len(data)
    ncols = len(data[0])
    start = nrows - 2, 1
    stop = 1, ncols - 2
    scores = {}
    i, j = start
    di, dj = (0, 1)  # facing east
    path = ((i, j, di, dj),)
    score = 0
    q = [(score, path)]
    while q:
        score, path = heappop(q)
        i, j, di, dj = path[-1]
        if path[-1] in path[:-1]:
            # have gone here before in the current path from same direction
            continue
        if (i, j) == stop:
            yield score, path
            continue
        if path[-1] in scores and scores[path[-1]] < score:
            # have reached this from same direction (in any path) cheaper
            continue
        scores[path[-1]] = score
        for dii, djj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (dii, djj) == (-di, -dj):
                # don't go back
                continue
            ii, jj = i + dii, j + djj
            if data[ii][jj] == "#":
                continue
            if (dii, djj) == (di, dj):
                # keep direction
                new_score = score + 1
            else:
                # turn
                new_score = score + 1001
            heappush(q, (new_score, path + ((ii, jj, dii, djj),)))


@watch.measure_time
def solve1(data):
    return min(score for score, path in iter_paths(data))


@watch.measure_time
def solve2(data):
    paths = [
        (score, set([(i, j) for i, j, di, dj in path]))
        for score, path in iter_paths(data)
    ]
    min_score = min(score for score, path in paths)
    best = [path for score, path in paths if score == min_score]
    tiles = set.union(*best)
    return len(tiles)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
