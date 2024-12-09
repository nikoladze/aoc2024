#!/usr/bin/env python

from tqdm.auto import tqdm
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.strip()


@watch.measure_time
def solve1(data):
    file_id = 0
    blocks = []
    for i, x in enumerate(data):
        if i % 2 == 0:
            blocks += [file_id] * int(x)
            file_id += 1
        else:
            blocks += ["."] * int(x)
    compacted = []
    for x in list(blocks):
        if len(blocks) == len(compacted):
            break
        while x == ".":
            x = blocks.pop()
        compacted.append(int(x))
    return sum(i * x for i, x in enumerate(compacted))


@watch.measure_time
def solve2(data):
    file_id = 0
    blocks = []
    spaces = {}
    file_pos = {}
    pos = 0
    for i, x in enumerate(data):
        if i % 2 == 0:
            blocks += [file_id] * int(x)
            file_pos[file_id] = pos
            file_id += 1
        else:
            blocks += ["."] * int(x)
            spaces[pos] = int(x)
        pos += int(x)

    #print(f"{spaces=}")

    data_sizes = [int(x) for x in data[::2]]

    def move(file_id, space_pos):
        file_size = data_sizes[file_id]
        for i in range(space_pos, space_pos + file_size):
            blocks[i] = file_id
        spaces[space_pos + file_size] = spaces[space_pos] - file_size
        del spaces[space_pos]
        for i in range(file_pos[file_id], file_pos[file_id] + file_size):
            blocks[i] = "."

    #print("".join(map(str, blocks)))

    #n_empty = len([x for x in blocks if x == "."])
    for file_id in tqdm(range(len(data_sizes) - 1, -1, -1), disable=False):
        #print(file_id)
        data_size = data_sizes[file_id]
        for space_pos, space_len in sorted(spaces.items(), key=lambda x: x[0]):
            if space_pos >= file_pos[file_id]:
                continue
            if space_len >= data_size:
                #print(f"move {file_id} to {space_pos}")
                move(file_id, space_pos)
                #assert len([x for x in blocks if x == "."]) == n_empty
                #input()
                #print("".join(map(str, blocks)))
                #print(spaces)
                break

    #print("".join(map(str, blocks)))
    return sum(i * x for i, x in enumerate(blocks) if x != ".")


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

# 24262669361508: too high
# part2: 8529293116363: too high
