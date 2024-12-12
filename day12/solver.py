#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


@watch.measure_time
def solve1(data):
    pos_cluster = {}
    clusters = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            #print(i, j, x)
            for di, dj in [(-1, 0), (0, -1)]:
                ii, jj = i + di, j + dj
                if ii < 0 or jj < 0 or i >= len(data) or j >= len(data[0]):
                    continue
                if x != data[ii][jj]:
                    continue
                if (i, j) not in pos_cluster:
                    pos_cluster[ii, jj].add((i, j))
                    pos_cluster[i, j] = pos_cluster[ii, jj]
                if pos_cluster[i, j] is not pos_cluster[ii, jj]:
                    # merge
                    pos_cluster[ii, jj].update(pos_cluster[i, j])
                    clusters.remove(pos_cluster[i, j])
                    for pos in pos_cluster[i, j]:
                        pos_cluster[pos] = pos_cluster[ii, jj]

            if (i, j) not in pos_cluster:
                cluster = set([(i, j)])
                pos_cluster[i, j] = cluster
                clusters.append(cluster)
                #print("new cluster")
            #input()
    total = 0
    for cluster in clusters:
        area = len(cluster)
        perimeter = 0
        for i, j in cluster:
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (i + di, j + dj) not in cluster:
                    perimeter += 1
        total += area * perimeter
        #print(f"{area} * {perimeter} = {area * perimeter}")
    return total

@watch.measure_time
def solve2(data):
    pos_cluster = {}
    clusters = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            #print(i, j, x)
            for di, dj in [(-1, 0), (0, -1)]:
                ii, jj = i + di, j + dj
                if ii < 0 or jj < 0 or i >= len(data) or j >= len(data[0]):
                    continue
                if x != data[ii][jj]:
                    continue
                if (i, j) not in pos_cluster:
                    pos_cluster[ii, jj].add((i, j))
                    pos_cluster[i, j] = pos_cluster[ii, jj]
                if pos_cluster[i, j] is not pos_cluster[ii, jj]:
                    # merge
                    pos_cluster[ii, jj].update(pos_cluster[i, j])
                    clusters.remove(pos_cluster[i, j])
                    for pos in pos_cluster[i, j]:
                        pos_cluster[pos] = pos_cluster[ii, jj]

            if (i, j) not in pos_cluster:
                cluster = set([(i, j)])
                pos_cluster[i, j] = cluster
                clusters.append(cluster)
                #print("new cluster")
            #input()
    total = 0
    for cluster in clusters:
        debug(cluster)
        area = len(cluster)
        border = set()
        border_i = {}
        border_j = {}
        for i, j in cluster:
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (i + di, j + dj) not in cluster:
                    # track borders in all x coords, y coords
                    border.add((i, j))
                    if dj != 0:
                        border_i.setdefault(dj, {}).setdefault(j, set()).add(i)
                    if di != 0:
                        border_j.setdefault(di, {}).setdefault(i, set()).add(j)
        print(border_i)
        print(border_j)
        sides = 0
        for border in [border_i, border_j]:
            for values_d in border.values():
                for values in values_d.values():
                    prev = None
                    for x in sorted(values):
                        if prev is None or abs(x - prev) != 1:
                            sides += 1
                        prev = x
        print(sides)
        total += sides * area
    return total

def debug(points):
    maxi = max(i for i, j in points)
    maxj = max(j for i, j in points)
    mini = min(i for i, j in points)
    minj = min(j for i, j in points)
    grid = [["." for j in range(maxj - minj + 1)] for i in range(maxi - mini + 1)]
    for i, j in points:
        grid[i - mini][j - minj] = "X"
    print()
    print("\n".join("".join(row) for row in grid))
    print()


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
