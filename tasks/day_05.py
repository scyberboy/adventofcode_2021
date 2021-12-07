import operator
import os
import re
import sys

import numpy as np


def read_input():
    # Read lines input
    # return two lists with points - starting and ending
    # each point is dict with keys "x" and "y"

    start_points = list()
    end_points = list()
    for line in sys.stdin:
        # "424,924 -> 206,706"
        mod_line = line.split()
        # ['424,924', '->', '206,706']

        # eliminate the "arrow"...
        del(mod_line[1])
        # ['424,924', '206,706']

        # put them in corresponding points list (as dict elem)
        sp_list = mod_line[0].split(",")
        ep_list = mod_line[1].split(",")

        sp_elem = {"x": int(sp_list[0]),
                   "y": int(sp_list[1])}
        ep_elem = {"x": int(ep_list[0]),
                   "y": int(ep_list[1])}

        start_points.append(sp_elem)
        end_points.append(ep_elem)

    return start_points, end_points


def count_overlapping_points(data, limit_val):
    # type:(np.ndarray, int) -> int
    # print("data.shape:", data.shape)
    # print("data.size:", data.size)
    # print("data:", data)
    # , format="%8d"
    # data.tofile("vents_map.txt", sep=" ")
    np.savetxt("vents_map-savetxt.txt", data, fmt="%3d")
    # , formatter={'int_kind': lambda x: "%8d" % x}
    # data_str = np.array2string(data, max_line_width=3000, threshold=100000, edgeitems=1000)
    # print("data_str:", data_str)

    # elem_sum = np.add.reduce(data.flatten(), where=operator.gt(data.flatten(), limit_val))
    # my_cnt_func = np.frompyfunc(len, 1, 1)
    # my_cnt = my_cnt_func.reduce(data.flatten(), where=operator.gt(data.flatten(), limit_val))
    # print("my_cnt_func:", my_cnt_func)
    # print("my_cnt:", my_cnt)

    reduced_array = data[operator.gt(data, limit_val)]
    np.savetxt("reduced_array-savetxt.txt", reduced_array, fmt="%3d")

    elem_cnt = reduced_array.size
    # print("reduced_array:", reduced_array)
    # print("elem_cnt:", elem_cnt)

    return elem_cnt


def fill_vents_map(empty_map, start_points, end_points):
    # type:(np.ndarray, list, list) -> np.ndarray
    # the map is initialized with zeros at creation
    # so, increment each point of it

    new_map = empty_map.copy()
    sp_len = len(start_points)
    ep_len = len(end_points)
    input_len = min(sp_len, ep_len)

    # print("empty_map.shape:", empty_map.shape)
    # print("new_map.shape:", new_map.shape)

    for idx in range(input_len):
        # 526,455 -> 590,455 - horizontal line (y1 == y2)
        # 134,976 -> 134,689 - vertical line (x1 == x2)

        # lines may go in both directions so, check the coordinates and "normalize" them
        # by assuring starting is always less than ending
        sp_x = min(start_points[idx]["x"], end_points[idx]["x"])
        sp_y = min(start_points[idx]["y"], end_points[idx]["y"])
        ep_x = max(start_points[idx]["x"], end_points[idx]["x"])
        ep_y = max(start_points[idx]["y"], end_points[idx]["y"])

        if sp_x == ep_x:
            # draw vertical
            for i in range(sp_y, ep_y + 1):
                new_map[sp_x][i] += 1
            # print("[{:4d}]\tdrawn ver line ({}, {}) -> ({}, {}): {}"
            #       .format(idx, sp_x, sp_y, ep_x, ep_y, new_map[sp_x][sp_y:ep_y+1]))
        else:
            # draw horizontal
            for i in range(sp_x, ep_x + 1):
                new_map[i][sp_y] += 1
            # print("[{:4d}]\tdrawn hor line ({}, {}) -> ({}, {}): {}"
            #       .format(idx, sp_x, sp_y, ep_x, ep_y, new_map.transpose()[sp_y][sp_x:ep_x+1]))

    return new_map


def find_solution_a(start_points, end_points):
    # type: (list, list) -> int
    """
    For now, consider only horizontal and vertical lines.
    Thus, filter only these where (s[x] = e[x] or s[y] = e[y])

    :return: Answer of the problem(a)
    """

    reduced_sp = [sp for _idx, sp in enumerate(start_points)
                  if sp["x"] == end_points[_idx]["x"]
                  or sp["y"] == end_points[_idx]["y"]]
    reduced_ep = [ep for _idx, ep in enumerate(end_points)
                  if ep["x"] == start_points[_idx]["x"]
                  or ep["y"] == start_points[_idx]["y"]]

    max_x = max([p["x"] for p in reduced_sp + reduced_ep])
    max_y = max([p["y"] for p in reduced_sp + reduced_ep])

    # print("Nr. reduced sp: {}, nr. reduced ep: {}".format(len(reduced_sp), len(reduced_ep)))
    # print("max X: {}, max Y: {}".format(max_x, max_y))

    empty_map = np.zeros((max_x+1, max_y+1), dtype=int)
    # print(empty_map.shape)

    filled_map = fill_vents_map(empty_map, reduced_sp, reduced_ep)
    # print("filled_map:", filled_map.tolist())
    # print("argmax(0):", filled_map.argmax(0))
    # print("argmax(1):", filled_map.argmax(1))

    answer = count_overlapping_points(filled_map, 1)

    return answer


def find_solution_b(data):
    # Find the last winning board

    # print("answer: {} <- number: {}, sum_unmarked: {}".format(answer, last_winning_num, sum_unmarked))
    pass


def do_main():

    start_points, end_points = read_input()
    # print("len start_points data:", len(start_points))
    # print("start_points:", start_points)
    # print("len end_points data:", len(end_points))
    # print("end_points:", end_points)

    result_a = find_solution_a(start_points, end_points)
    print("result_a:", result_a)

    # result_b = find_solution_b(vent_lines)
    # print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
