#!/usr/bin/env python

from itertools import chain
from pathlib import Path
import graphviz
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    initial, instructions = raw_data.strip().split("\n\n")
    initial = [line.split(": ") for line in initial.splitlines()]
    initial = {k: int(v) for k, v in initial}
    instructions = [line.split(" -> ") for line in instructions.splitlines()]
    instructions = [(left.split(), right) for left, right in instructions]
    return initial, instructions


@watch.measure_time
def solve1(data):
    initial, instructions = data
    results = dict(initial)
    graph = {right: left for left, right in instructions}
    zs = reversed(sorted(key for key in graph if key.startswith("z")))

    def run(key):
        if key in results:
            return results[key]
        ins = graph[key]
        match ins:
            case a, "OR", b:
                res = run(a) | run(b)
            case a, "XOR", b:
                res = run(a) ^ run(b)
            case a, "AND", b:
                res = run(a) & run(b)
            case _:
                assert False
        results[key] = res
        return res

    digits = []
    for z in zs:
        digits.append(str(run(z)))

    return int("".join(digits), 2)


@watch.measure_time
def solve2(data, mode="ADD"):
    initial, instructions = data
    ins_graph = {b: a for a, b in instructions}

    def check(zkey):
        # full adder:
        # -----------
        # x xor y = a1
        # x and y = a2
        # a1 xor cin = z
        # a1 and cin = a3
        # a2 or a3 = cout
        a, op, b = ins_graph[zkey]
        if op != "XOR":
            print(f"problem with {zkey}")
            return
        for ai in [a, b]:
            if ins_graph[ai][1] == "XOR":
                a1 = ai
                break
        else:
            print(f"problem with {a} or {b}")
            return
        cin = [ai for ai in [a, b] if ai is not a1][0]
        a, op, b = ins_graph[a1]
        assert op == "XOR"
        if set([ai[0] for ai in [a, b]]) != {"x", "y"}:
            print(f"problem with {a1}")

    print()
    print("Part2 is a bit manual")
    print("=====================")
    for i in range(1, 45):  # 0 is fine and only a half adder ;)
        check(f"z{i:02d}")

    g = graphviz.Digraph()
    for key in ins_graph:
        a, op, b = ins_graph[key]
        a, b, key = [a], [b], [key]
        for x in [a, b, key]:
            if x[0] in ins_graph:
                x[0] = f"{ins_graph[x[0]][1]} - {x[0]}"
        a, b, key = a[0], b[0], key[0]
        g.edge(a, key)
        g.edge(b, key)
    g.render("graph")

    print(
        "now look at the graph (graph.pdf) and figure out that we need to swap the following:"
    )

    swaps = (
        ("z09", "gwh"),
        ("wbw", "wgb"),
        ("rcb", "z21"),
        ("z39", "jct"),
    )

    print(swaps)

    return ",".join(sorted(chain(*swaps)))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
