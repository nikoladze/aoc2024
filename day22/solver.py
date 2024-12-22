#!/usr/bin/env python

from pathlib import Path
from tqdm.auto import tqdm
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return list(map(int, raw_data.strip().splitlines()))


def mix(a, b):
    return a ^ b


def prune(x):
    return x % 16777216


def step(x):
    x = prune(mix(x * 64, x))
    x = prune(mix(x // 32, x))
    x = prune(mix(x * 2048, x))
    return x


def steps(x, n=2000):
    for i in range(n + 1):
        yield x
        x = step(x)


@watch.measure_time
def solve1(data):
    return sum(list(steps(x))[-1] for x in data)


@watch.measure_time
def solve2(data):
    sequences = [list(steps(x)) for x in data]
    prices = [[int(str(x)[-1]) for x in s] for s in sequences]
    diffs = [[b - a for a, b in zip(s, s[1:])] for s in prices]
    dicts = []
    for sub_diffs, sub_prices in zip(diffs, prices):
        d = {}
        for start in range(4, len(sub_diffs) + 1):
            diff_seq = tuple(sub_diffs[start - 4 : start])
            if diff_seq not in d:
                d[diff_seq] = sub_prices[start]
        dicts.append(d)

    # only iterate over sequences that exist at all
    bananas = []
    for diff_seq in tqdm(set.union(*(set(d.keys()) for d in dicts))):
        bananas.append(sum(d.get(diff_seq, 0) for d in dicts))

    return max(bananas)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
