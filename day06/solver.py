#!/usr/bin/env python

from tqdm.auto import tqdm
from collections import deque
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
    i, j = get_start(data)
    direction_dict = {
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
        "^": (-1, 0),
    }
    directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])
    while directions[0] != direction_dict[data[i][j]]:
        directions.rotate(-1)
    nrows = len(data)
    ncols = len(data[0])

    visited = set()
    di, dj = directions[0]
    while i >= 0 and j >= 0 and i < nrows and j < ncols:
        if data[i][j] == "#":
            directions.rotate(-1)
            i, j = i - di, j - dj  # go back
            di, dj = directions[0]
        else:
            visited.add((i, j))
        i, j = i + di, j + dj

    # debug = [[x for x in row] for row in data]
    # for i, j in visited:
    #     debug[i][j] = "X"
    # print("\n".join("".join(row) for row in debug))

    return len(visited)


@watch.measure_time
def solve2(data):
    i, j = get_start(data)
    direction_dict = {
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
        "^": (-1, 0),
    }
    nrows = len(data)
    ncols = len(data[0])

    def is_loop(data, obstacle):
        i, j = get_start(data)
        directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])
        while directions[0] != direction_dict[data[i][j]]:
            directions.rotate(-1)
        visited = set()
        di, dj = directions[0]
        while i >= 0 and j >= 0 and i < nrows and j < ncols:
            if data[i][j] == "#" or (i, j) == obstacle:
                directions.rotate(-1)
                i, j = i - di, j - dj  # go back
                di, dj = directions[0]
            else:
                visited.add((i, j, di, dj))
            i, j = i + di, j + dj
            if (i, j, di, dj) in visited:
                return True
        return False

    total = 0
    for i in tqdm(range(nrows)):
        for j in range(ncols):
            if data[i][j] != ".":
                continue
            if is_loop(data, obstacle=(i, j)):
                total += 1
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
