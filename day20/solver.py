#!/usr/bin/env python

from collections import Counter
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def search(data, s):
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == s:
                return i, j


@watch.measure_time
def solve1(data):
    S = search(data, "S")
    E = search(data, "E")
    i, j = S
    k = 0
    track = {}
    while (i, j) != E:
        track[i, j] = k
        k += 1
        for i, j in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if data[i][j] != "#" and (i, j) not in track:
                break

    total = 0
    for (i, j), score in track.items():
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ii, jj = i + di, j + dj
            iii, jjj = ii + di, jj + dj
            if iii < 0 or jjj < 0 or iii >= len(data) or jjj >= len(data[0]):
                continue
            if data[ii][jj] != "#":
                continue
            if data[iii][jjj] != ".":
                continue
            prev_score = track[iii, jjj]
            saving = prev_score - (score + 2)
            if saving >= 100:
                total += 1
    return total


@watch.measure_time
def solve2(data):
    S = search(data, "S")
    E = search(data, "E")
    i, j = S
    k = 0
    track = {}
    while True:
        track[i, j] = k
        if (i, j) == E:
            break
        k += 1
        for i, j in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if data[i][j] != "#" and (i, j) not in track:
                break

    cheats = {}

    def find_cheats(i_start, j_start, score, max_t=20):
        q = [(i_start, j_start, 0)]
        visited = set()
        while q:
            i, j, t = q.pop()
            visited.add((i, j, t))
            if data[i][j] != "#":
                prev_score = track[i, j]
                saving = prev_score - (score + t)
                key = (i_start, j_start, i, j)
                if key not in cheats or cheats[key] < saving:
                    cheats[key] = saving
            if t == max_t:
                continue
            for i, j in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if i < 0 or j < 0 or i >= len(data) or j >= len(data[0]):
                    continue
                if (i, j, t + 1) in visited:
                    continue
                key = (i, j, t + 1)
                visited.add(key)
                q.append(key)

    for (i, j), score in track.items():
        print(i, j, end="\r")
        find_cheats(i, j, score)

    c = Counter(cheats.values())
    return sum(saving >= 100 for saving in cheats.values())


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
