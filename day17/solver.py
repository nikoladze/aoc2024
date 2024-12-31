#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    registers, program = raw_data.strip().split("\n\n")
    a, b, c = [int(r.split()[-1]) for r in registers.splitlines()]
    return (a, b, c), list(map(int, program.split()[-1].split(",")))


@watch.measure_time
def solve1(data):
    (a, b, c), program = data
    out = run(program, a, b, c)
    return ",".join(map(str, out))


def run(program, a, b=0, c=0, debug=False):

    _debug = debug

    def debug(x):
        if _debug:
            print(x)

    def combo(operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return a
        if operand == 5:
            return b
        if operand == 6:
            return c
        assert False

    def div(a, b):
        return a // (2**b)

    debug(f"{a=}")

    i = 0
    out = []
    while i >= 0 and i < len(program):
        ins = program[i]
        operand = program[i + 1]
        match ins:
            case 0:  # adv
                debug(f"a = div(a, {combo(operand)}) = {div(a, combo(operand))}")
                a = div(a, combo(operand))
            case 1:  # bxl
                debug(f"b = b ^ {operand} = {b ^ operand}")
                b = b ^ operand
            case 2:  # bst
                debug(f"b = {combo(operand)} % 8 = {combo(operand) % 8}")
                b = combo(operand) % 8
            case 3:  # jnz
                if a != 0:
                    i = operand
                    continue
            case 4:  # bxc
                debug(f"b = b ^ c = {b ^ c}")
                b = b ^ c
            case 5:  # out
                debug(f"output from {i=}: {combo(operand)} % 8 = {combo(operand) % 8}")
                out.append(combo(operand) % 8)
            case 6:  # bdv
                debug(f"b = div(a, {combo(operand)}) = {div(a, combo(operand))}")
                b = div(a, combo(operand))
            case 7:  # cdv
                debug(
                    f"c = div(a, combo({operand})) "
                    f"= div(a, {combo(operand)}) "
                    f"= {div(a, combo(operand))}"
                )
                c = div(a, combo(operand))
        i += 2

    return out


def search(program, a, bit_pos, slice, b=0, c=0):
    base = a
    for i in range(1 << 3):
        a = base
        # overwrite 3 bits from bit_pos to the left (more significant)
        for j in range(3):
            bit = i & 1
            a |= bit << (bit_pos + j)
            i >>= 1
        res = run(program, a)
        if res[slice] == program[slice]:
            yield a


def find_solution(program, n=45):
    """
    The program effectively does (while a != 0)
    b = a % 8
    b = b ^ 2
    c = a // (2**b)
    b = b ^ 3
    b = b ^ c
    output = b
    a //= 8

    2^45 is the smallest number that produces enough outputs -> start from this

    so the last output only depends on the 8 most significant bits,
    the second to last output on the 16, etc - that means
    * we can iterate through backwards and only need to check 2**3 = 8 inputs for every output position
    * this produces candidates
    * for every earlier output we need to check based on all previous candidates
    """
    start = 1 << n
    candidates = [start]
    for i, bit_pos in enumerate(range(n - 3, -1, -3), 1):
        new_candidates = []
        for candidate in candidates:
            for sub in search(program, candidate, bit_pos, slice(-i - 1, None)):
                new_candidates.append(sub)
        candidates = new_candidates
    return candidates


@watch.measure_time
def solve2(data):
    (a, b, c), program = data

    # print()
    # print("Program logic:")
    # print("============================")
    # run(program, a=2**10 + 42, debug=True)
    # print()

    return min(find_solution(program))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
