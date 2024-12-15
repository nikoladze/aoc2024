#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def find_clusters(data):
    pos_cluster = {}
    clusters = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            for di, dj in [(-1, 0), (0, -1)]:
                ii, jj = i + di, j + dj
                if ii < 0 or jj < 0 or i >= len(data) or j >= len(data[0]):
                    continue
                elif x != data[ii][jj]:
                    continue
                elif (i, j) not in pos_cluster:
                    # add to neighboring cluster
                    pos_cluster[ii, jj].add((i, j))
                    pos_cluster[i, j] = pos_cluster[ii, jj]
                elif pos_cluster[i, j] is not pos_cluster[ii, jj]:
                    # merge with neighboring cluster
                    pos_cluster[ii, jj].update(pos_cluster[i, j])
                    clusters.remove(pos_cluster[i, j])
                    for pos in pos_cluster[i, j]:
                        pos_cluster[pos] = pos_cluster[ii, jj]
            if (i, j) not in pos_cluster:
                cluster = set([(i, j)])
                pos_cluster[i, j] = cluster
                clusters.append(cluster)
    return clusters


@watch.measure_time
def solve1(data):
    clusters = find_clusters(data)
    total = 0
    for cluster in clusters:
        area = len(cluster)
        perimeter = 0
        for i, j in cluster:
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (i + di, j + dj) not in cluster:
                    perimeter += 1
        total += area * perimeter
    return total


@watch.measure_time
def solve2(data):
    clusters = find_clusters(data)
    total = 0
    for cluster in clusters:
        area = len(cluster)
        borders = {}
        for i, j in cluster:
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (i + di, j + dj) not in cluster:
                    # group borders by direction and by common
                    # coordinates in i (horizontal borders)
                    # and j (vertical borders) coordinates
                    if dj != 0:
                        common = j
                        varying = i
                    elif di != 0:
                        common = i
                        varying = j
                    borders.setdefault((di, dj, common), set()).add(varying)
        sides = 0
        for values in borders.values():
            # find groups of connected border points
            prev = None
            for x in sorted(values):
                if prev is None or abs(x - prev) != 1:
                    sides += 1
                prev = x
        total += sides * area
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
