#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    grid, instructions = raw_data.strip().split("\n\n")
    instructions = instructions.replace("\n", "")
    grid = grid.splitlines()
    return grid, instructions


def get_start(grid):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "@":
                return i, j


@watch.measure_time
def solve1(data):
    grid, instructions = data
    grid = [[c for c in row] for row in grid]
    i, j = get_start(grid)
    for instruction in instructions:
        di, dj = {
            "^": (-1, 0),
            "v": (1, 0),
            "<": (0, -1),
            ">": (0, 1),
        }[instruction]
        ii, jj = i + di, j + dj
        if grid[ii][jj] == ".":
            grid[i][j] = "."
            grid[ii][jj] = "@"
            i, j = ii, jj
            continue
        elif grid[ii][jj] == "#":
            continue
        elif grid[ii][jj] == "O":
            iii, jjj = ii, jj
            while True:
                iii, jjj = iii + di, jjj + dj
                if grid[iii][jjj] == ".":
                    grid[iii][jjj] = "O"
                    grid[ii][jj] = "@"
                    grid[i][j] = "."
                    i, j = ii, jj
                    break
                elif grid[iii][jjj] == "#":
                    break
                elif grid[iii][jjj] == "O":
                    continue

    total = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "O":
                total += 100 * i + j
    return total


def find_movable(grid, i, j, di, dj):
    q = [(i + di, j + dj)]
    movable = set()
    while q:
        ii, jj = q.pop()
        if grid[ii][jj] == "#":
            return []
        elif grid[ii][jj] == ".":
            continue
        elif (ii, jj) in movable:
            continue
        elif grid[ii][jj] == "[":
            movable.add((ii, jj))
            q.append((ii + di, jj + dj))
            q.append((ii, jj + 1))
        elif grid[ii][jj] == "]":
            movable.add((ii, jj))
            q.append((ii + di, jj + dj))
            q.append((ii, jj - 1))
    return movable


def move(grid, movable, di, dj):
    new = {(i + di, j + dj): grid[i][j] for i, j in movable}
    for i, j in movable:
        if (i, j) not in new:
            grid[i][j] = "."
    for (i, j), c in new.items():
        grid[i][j] = c


@watch.measure_time
def solve2(data):
    grid, instructions = data
    new_grid = []
    for row in grid:
        new_row = []
        for c in row:
            if c == "#":
                new_row += ["#", "#"]
            elif c == "O":
                new_row += ["[", "]"]
            elif c == ".":
                new_row += [".", "."]
            elif c == "@":
                new_row += ["@", "."]
        new_grid.append(new_row)
    grid = new_grid

    i, j = get_start(grid)
    for instruction in instructions:
        di, dj = {
            "^": (-1, 0),
            "v": (1, 0),
            "<": (0, -1),
            ">": (0, 1),
        }[instruction]
        ii, jj = i + di, j + dj
        if grid[ii][jj] == ".":
            grid[i][j] = "."
            grid[ii][jj] = "@"
            i, j = ii, jj
            continue
        elif grid[ii][jj] == "#":
            continue
        elif grid[ii][jj] in "[]":
            movable = find_movable(grid, i, j, di, dj)
            if movable:
                move(grid, movable, di, dj)
                grid[i][j] = "."
                grid[ii][jj] = "@"
                i, j = ii, jj

    total = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "[":
                total += 100 * i + j
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
