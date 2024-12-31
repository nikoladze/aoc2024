#!/usr/bin/env python

from functools import cache
from random import shuffle
from itertools import product
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def sign(x):
    return 1 if x > 0 else -1


def find_moves(start, end, coordinates):
    out = []
    di = end[0] - start[0]
    dj = end[1] - start[1]
    path = []
    i, j = start
    valid = True
    # move along i first
    for ddi in range(abs(di)):
        i += sign(di)
        if (i, j) not in coordinates.values():
            valid = False
        path.append("v" if di > 0 else "^")
    for ddj in range(abs(dj)):
        j += sign(dj)
        if (i, j) not in coordinates.values():
            valid = False
        path.append(">" if dj > 0 else "<")
    if valid:
        out.append(path)
    old_path = path
    path = []
    i, j = start
    valid = True
    # move along j first
    for ddj in range(abs(dj)):
        j += sign(dj)
        if (i, j) not in coordinates.values():
            valid = False
        path.append(">" if dj > 0 else "<")
    for ddi in range(abs(di)):
        i += sign(di)
        if (i, j) not in coordinates.values():
            valid = False
        path.append("v" if di > 0 else "^")
    if path != old_path and valid:
        out.append(path)
    return out


def to_coord_dict(*rows):
    d = {}
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if not c.isspace():
                d[c] = i, j
    return d


numeric_coordinates = to_coord_dict(
    "789",
    "456",
    "123",
    " 0A",
)

directional_coordinates = to_coord_dict(
    " ^A",
    "<v>",
)


def random_move_sequence(code, coordinates, start="A"):
    "i'm not proud of this, but here we go"
    out = []
    for c in code:
        end = c  # just one step
        possibilities = find_moves(coordinates[start], coordinates[end], coordinates)

        # pick a random option
        shuffle(possibilities)
        out += possibilities[0] + ["A"]

        start = c
    return out


@watch.measure_time
def solve1(data, nrobots=2):
    totals = set()
    for i in range(1000):  # try 1000 random combinations
        total = 0
        for code in data:
            x = random_move_sequence(code, numeric_coordinates)
            for i in range(nrobots):
                x = random_move_sequence(x, directional_coordinates)
            total += len(x) * int(code[:-1])
        totals.add(total)
    return min(totals)


def find_shortest(code, nrobots=2, include_first=False, n_samples=100):
    "no idea how many steps in the future (`n_robots`) i'll have to look, seems 2-3 is fine"
    out = []
    for i in range(n_samples):
        x = code
        seqs = []
        if include_first:
            x = random_move_sequence(code, numeric_coordinates)
            seqs.append(x)
        for i in range(nrobots):
            x = random_move_sequence(x, directional_coordinates)
            seqs.append(x)
        seqs = ["".join(x) for x in seqs]
        out.append(seqs)
    return min(out, key=lambda x: len(x[-1]))


def solve(data, nrobots=25):
    start_sequences = []
    for code in data:
        shortest = find_shortest(code, nrobots=3, include_first=True)
        start_sequences.append(shortest[0])

    # lookup shortest expansion for every combination of 2 keys
    lookup = {}
    keys = directional_coordinates.keys()
    for c1, c2 in product(keys, keys):
        key = c1 + c2
        lookup[key] = find_shortest(key, nrobots=3, include_first=False)[0]

    def expand(seq, first=True):
        out = []
        for start, end in zip(seq, seq[1:]):
            lu = lookup[start + end]
            pos = lu.find("A") + 1
            if first:
                out.append(lu[:pos])
            out.append(lu[pos:])
            first = False
        return "".join(out)

    @cache
    def count_len(seq, steps, first=True):
        if steps == 0:
            return len(seq) - 1
        seq = expand(seq, first=first)
        total = 0
        chunks = seq.split("A")
        for sub in chunks:
            total += count_len("A" + sub + "A", steps=steps - 1, first=False)
        return total - 1  # don't quite get that off by one error yet

    total = 0
    for code, seq in zip(data, start_sequences):
        n = count_len(seq, steps=nrobots)
        total += n * int(code[:-1])
    return total


@watch.measure_time
def solve2(data):
    out = []
    # sometimes still not the right answer, so run the whole thing 30x with different random seed ...
    for __ in range(30):
        out.append(solve(data, nrobots=25))
        print(out[-1], end="\r")
    return min(out)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
