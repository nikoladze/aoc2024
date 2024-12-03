#!/usr/bin/env python

import re
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data


@watch.measure_time
def solve1(data):
    total = 0
    for sub in re.findall(r"mul\([0-9]+,[0-9]+\)", data):
        a, b = sub.split("(")[1].split(")")[0].split(",")
        total += int(a) * int(b)
    return total


@watch.measure_time
def solve2(data):
    total = 0
    enabled = True
    for sub in re.findall(r"(?:mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\))", data):
        if sub == "do()":
            enabled = True
        elif sub == "don't()":
            enabled = False
        elif enabled:
            a, b = sub.split("(")[1].split(")")[0].split(",")
            total += int(a) * int(b)
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
