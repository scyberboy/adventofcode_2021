import itertools
import os
import re
import sys
import time

import numpy as np


def read_input() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """

    """
    # Read lines input:
    # 6,10
    # 0,14
    # 9,10
    # 0,3
    # 1,10
    # 2,14
    # 8,10
    # 9,0
    #
    # fold along y=7
    # fold along x=5

    # keep the dot's as list of two elements tuple (int, int) - (0, 5)
    dots = list()
    # instructions as list of two elements (int, int) - (0, 7), where first is (0->x or 1->y), second is the axis
    instructions = list()

    while True:
        line = sys.stdin.readline()
        # print("1st while, line: '{}'".format(line))
        if line == "\n" or line == "":
            break
        group = line.strip().split(",")
        dots.append((int(group[0]), int(group[1])))

    while True:
        line = sys.stdin.readline()
        # print("2nd while, line: '{}'".format(line))
        if line == "\n" or line == "":
            break
        last_group = line.strip().split()[2]
        instructions.append((0 if last_group.split("=")[0] == "x" else 1, int(last_group.split("=")[1])))

    # return two lists:
    # - dots
    # - folding instructions
    return dots, instructions


def fold_map(map_to_fold: np.ndarray, y_limit, x_limit, axis: int, value: int):
    new_map = np.full(shape=(y_limit, x_limit), dtype=bool, fill_value=False)
    # print("size({}) map_to_fold.shape: {}".format(map_to_fold.size, map_to_fold.shape))
    # print("size({}) new_map.shape: {}".format(new_map.size, new_map.shape))

    # y_limit, x_limit = map_to_fold.shape

    if axis == 0:  # fold along x (horizontal)
        # y -> constant (full)
        min_y = 0
        max_y = y_limit
        min_x = 0
        max_x = value
        # print("axis: {}, value: {}".format(axis, value))
        # print("min_y: {}, max_y: {}".format(min_y, max_y))
        # print("min_x: {}, max_x: {}".format(min_x, max_x))

        for y, x in itertools.product(range(min_y, max_y), range(min_x, max_x), repeat=1):
            # target_x = x_limit - x - 1
            target_x = max_x + (max_x - x)
            # print("target_x: {}, x: {}, y: {}".format(target_x, x, y))
            if target_x >= x_limit:
                # the target is outside the map (i.e. the fold line is on the right from the middle)
                # so, consider the original element value only
                elem_val = map_to_fold[y, x] or False
            else:
                elem_val = map_to_fold[y, x] or map_to_fold[y, target_x]

            new_map[y, x] = elem_val

    else:  # 1, fold along y (vertical)
        # x -> constant (full)
        min_y = 0
        max_y = value
        min_x = 0
        max_x = x_limit
        # print("axis: {}, value: {}".format(axis, value))
        # print("min_y: {}, max_y: {}".format(min_y, max_y))
        # print("min_x: {}, max_x: {}".format(min_x, max_x))

        for y, x in itertools.product(range(min_y, max_y), range(min_x, max_x), repeat=1):
            # target_y = y_limit - y - 1
            target_y = max_y + (max_y - y)
            # print("target_y: {}, x: {}, y: {}".format(target_y, x, y))
            if target_y >= y_limit:
                # the target is outside the map (i.e. the fold line is below the middle)
                # so, consider the original element value only
                elem_val = map_to_fold[y, x] or False
            else:
                elem_val = map_to_fold[y, x] or map_to_fold[target_y, x]

            new_map[y, x] = elem_val

    return new_map


def find_solution_a(trans_map: np.ndarray, instruction: list[tuple[int, int]], nr_instr=1):
    map_list = list()
    map_list.append(trans_map)
    ini_y, ini_x = trans_map.shape

    max_y = ini_y
    max_x = ini_x

    for idx, (axis, value) in enumerate(instruction[:nr_instr]):
        folded = fold_map(map_list[idx], max_y, max_x, axis, value)
        max_y = min(ini_y, value if axis == 1 else max_y)
        max_x = min(ini_x, value if axis == 0 else max_x)
        folded = folded[:max_y, :max_x]
        # print("folded map, size: {}, shape: {}, max_y: {}, max_x: {}".format(folded.size, folded.shape, max_y, max_x))
        map_list.append(folded)

    true_cntr = 0
    # print("will count thru folded map({})({}), max_y: {}, max_x: {}".format(nr_instr, len(map_list), max_y, max_x))
    for y, x in itertools.product(range(max_y), range(max_x), repeat=1):
        # print("y: {}, x: {} -> {}".format(y, x, map_list[nr_instr][y, x]))
        true_cntr += (1 if map_list[nr_instr][y, x] else 0)
        # print("counter: {}".format(true_cntr))

    if nr_instr > 1:
        # for solution (b) we indeed need the visual representation of the final folded map (6, 40)
        print("---------- solution b (last)--------------")
        res_str = np.array_str(map_list[-1][:max_y, :max_x], max_line_width=(max_x*7), )
        print(res_str.replace("  ", " ").replace("True", "#").replace("False", "."))
        print("------------------------------------")

    return true_cntr


def find_solution_b():
    pass


def fill_trans_map(trans_map: np.ndarray, dots: list[tuple[int, int]]):
    for x, y in dots:
        trans_map[y, x] = True


def do_main():
    prev_time = time.process_time()

    print("start reading input...")
    dots, instructions = read_input()
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("input dots: {}".format(dots))
    # print("input instructions: {}".format(instructions))

    max_x = max([x for x, _ in dots])
    max_y = max([y for _, y in dots])

    trans_map = np.full(shape=(max_y+1, max_x+1), dtype=bool, fill_value=False)
    # print("np.ndarray trans_map:\n{}".format(trans_map))

    fill_trans_map(trans_map, dots)
    # print("np.ndarray filled trans_map({}):\n{}".format(trans_map.shape, trans_map))

    # print("nr True elems in trans_map:\n{}".format(trans_map[trans_map].size))

    print("find_solution_a...")
    result_a = find_solution_a(trans_map, instructions)
    print("result_a:", result_a)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_b...")
    result_b = find_solution_a(trans_map, instructions, len(instructions))
    print("result_b:", result_b)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    print("[{}] took: {} sec.".format(cur_time, diff))


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
