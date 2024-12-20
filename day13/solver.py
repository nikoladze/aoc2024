#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


def parse_button(s):
    return tuple([int(t.split("+")[1]) for t in s.split(", ")])


@watch.measure_time
def parse(raw_data):
    blocks = raw_data.strip().split("\n\n")
    machines = []
    for block in blocks:
        a, b, prize = [line.split(": ")[1] for line in block.splitlines()]
        a, b = parse_button(a), parse_button(b)
        prize = tuple([int(t.split("=")[1]) for t in prize.split(", ")])
        machines.append((a, b, prize))
    return machines


class NotDivisibleError(Exception):
    pass


def ensure_div(a, b):
    if a % b != 0:
        raise NotDivisibleError(f"{a} not divisible by {b}")
    return a // b


def solve(data, shift=0):
    """
    x = c * xa + d * xb
    y = c * ya + d * yb

    d = (x - c * xa) / xb = x / xb - xa / xb * c
    d = (y - c * ya) / yb = y / yb - ya / yb * c

    x / xb - c * xa / xb = y / yb - c * ya / yb
    x / xb - y / yb = c * (xa / xb - ya / yb)
    -> c = (x / xb - y / yb) / (xa / xb - ya / yb)
         = (x * yb - y * xb) / (xa * yb - ya * xb)
    """
    total = 0
    for (xa, ya), (xb, yb), (x, y) in data:
        x += shift
        y += shift
        try:
            c = ensure_div(x * yb - y * xb, xa * yb - ya * xb)
            d = ensure_div(x - c * xa, xb)
        except NotDivisibleError:
            continue
        total += c * 3 + d
    return total


@watch.measure_time
def solve1(data):
    return solve(data)


@watch.measure_time
def solve2(data):
    return solve(data, shift=10000000000000)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
