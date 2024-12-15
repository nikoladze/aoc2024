#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return [
        tuple(
            [tuple(map(int, chunk.split("=")[1].split(","))) for chunk in line.split()]
        )
        for line in raw_data.strip().splitlines()
    ]


@watch.measure_time
def solve1(data, width=101, height=103):
    robots = [[pos, v] for pos, v in data]
    for step in range(100):
        for robot in robots:
            (x, y), (vx, vy) = robot
            x = (x + vx) % width
            y = (y + vy) % height
            robot[0] = (x, y)
    tl, tr, bl, br = 0, 0, 0, 0
    for (x, y), __ in robots:
        if x == width // 2 or y == height // 2:
            continue
        left = x < width // 2
        top = y < height // 2
        if top and left:
            tl += 1
        if top and not left:
            tr += 1
        if not top and left:
            bl += 1
        if not top and not left:
            br += 1
    return tl * tr * bl * br


def find_clusters(coords, width, height):
    coords = set(coords)
    pos_cluster = {}
    clusters = []
    for x, y in sorted(coords, key=lambda x: (x[1], x[0])):
        for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0)]:
            xx, yy = x + dx, y + dy
            if xx < 0 or yy < 0 or x >= width or y >= height:
                continue
            if (xx, yy) not in coords:
                continue
            if (x, y) not in pos_cluster:
                # add to neighboring cluster
                pos_cluster[xx, yy].add((x, y))
                pos_cluster[x, y] = pos_cluster[xx, yy]
            if pos_cluster[x, y] is not pos_cluster[xx, yy]:
                # merge with neighboring cluster
                pos_cluster[xx, yy].update(pos_cluster[x, y])
                clusters.remove(pos_cluster[x, y])
                for pos in pos_cluster[x, y]:
                    pos_cluster[pos] = pos_cluster[xx, yy]
        if (x, y) not in pos_cluster:
            cluster = set([(x, y)])
            pos_cluster[x, y] = cluster
            clusters.append(cluster)
    return clusters


@watch.measure_time
def solve2(data, width=101, height=103):
    robots = [[pos, v] for pos, v in data]
    candidates = []
    for step in range(1, 20000):
        for robot in robots:
            (x, y), (vx, vy) = robot
            x = (x + vx) % width
            y = (y + vy) % height
            robot[0] = (x, y)
        clusters = find_clusters([(x, y) for (x, y), __ in robots], width, height)
        for cluster in clusters:
            if len(cluster) > 100:
                return step


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
