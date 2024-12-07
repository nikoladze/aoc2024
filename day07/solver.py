#!/usr/bin/env python

from operator import mul, add
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        result, operands = line.split(": ")
        operands = tuple(map(int, operands.split()))
        out.append((int(result), operands))
    return out


def is_possible(result, operands, operators):
    if len(operands) == 1:
        return operands[0] == result
    for operator in operators:
        a, b = operands[:2]
        if is_possible(result, (operator(a, b),) + operands[2:], operators):
            return True
    return False


@watch.measure_time
def solve1(data, operators=(mul, add)):
    total = 0
    for result, operands in data:
        if is_possible(result, operands, operators):
            total += result
    return total


def concat(a, b):
    return int(str(a) + str(b))


@watch.measure_time
def solve2(data):
    return solve1(data, operators=(mul, add, concat))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()


# 5031247864455: too low
