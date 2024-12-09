#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return list(map(int, raw_data.strip()))


@watch.measure_time
def solve1(data):
    file_id = 0
    blocks = []
    for i, x in enumerate(data):
        if i % 2 == 0:
            blocks += [file_id] * x
            file_id += 1
        else:
            blocks += ["."] * x
    compacted = []
    for x in list(blocks):
        if len(blocks) == len(compacted):
            break
        while x == ".":
            x = blocks.pop()
        compacted.append(x)
    return sum(i * x for i, x in enumerate(compacted))


@watch.measure_time
def solve2(data):
    blocks = []
    space_pos_len = {}
    file_id_pos = {}
    file_id = 0
    pos = 0
    for i, x in enumerate(data):
        if i % 2 == 0:
            blocks += [file_id] * x
            file_id_pos[file_id] = pos
            file_id += 1
        else:
            blocks += ["."] * x
            space_pos_len[pos] = x
        pos += x

    data_sizes = [x for x in data[::2]]

    # small optimization: keep a sorted list of space positions
    sorted_space_pos = sorted(space_pos_len)

    def move(file_id, space_pos):
        file_size = data_sizes[file_id]

        # put file to new space
        for i in range(space_pos, space_pos + file_size):
            blocks[i] = file_id
        # make space at old position
        for i in range(file_id_pos[file_id], file_id_pos[file_id] + file_size):
            blocks[i] = "."

        # update space position and length
        new_pos = space_pos + file_size
        space_pos_len[new_pos] = space_pos_len[space_pos] - file_size
        del space_pos_len[space_pos]
        sorted_space_pos.remove(space_pos)
        sorted_space_pos.append(new_pos)
        sorted_space_pos.sort()

    for file_id, data_size in reversed(list(enumerate(data_sizes))):
        for space_pos in list(sorted_space_pos):
            space_len = space_pos_len[space_pos]
            if space_pos >= file_id_pos[file_id]:
                break
            if space_len >= data_size:
                move(file_id, space_pos)
                break

    return sum(i * x for i, x in enumerate(blocks) if x != ".")


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
